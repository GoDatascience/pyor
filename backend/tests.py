import json
import os
import unittest
from typing import IO, List

from io import FileIO, BytesIO
from unittest.mock import patch, MagicMock

from flask.testing import FlaskClient
from mrq import config, context
from mrq.context import set_current_config
from mrq.utils import load_class_by_path
from pymongo.collection import Collection
from pymongo.database import Database
from werkzeug.datastructures import FileStorage

import mreq
from mreq import app
from mreq.controllers.tasks import FIELD_NAME, FIELD_PARAM_DEFINITIONS, FIELD_SCRIPT_FILE, FIELD_AUXILIAR_FILES, \
    FIELD_PARAMS, FIELD_QUEUE
from mreq.models import Task
import mreq.services

import shutil

from mreq.services import R_TASK

EXCLUDED_KEYS = ["last_modified"]

context.setup_context(file_path="workers/mrqconfig.py")
database: Database = context.connections.mongodb_jobs


class BaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["MREQ_DATA"] = os.path.join(os.environ["MREQ_DATA"], "tests")

    def setUp(self):
        os.chdir(os.environ["MREQ_BACKEND"])
        shutil.rmtree(os.path.join(os.environ["MREQ_DATA"], "tasks"), ignore_errors=True)
        for collection_name in database.collection_names(False):
            database[collection_name].drop()


class TasksExecutionTests(BaseTests):

    def test_python_slow_fib(self):
        # given
        task = create_task("slowbix", 'samples/slow_fib.py')

        # when
        mreq.services.enqueue_job(task, {"n": 20}, "sequential")
        result = start_worker()

        # then
        self.assertEqual(result, 5)

    def test_r_randombox(self):
        # given
        task = create_task("randombox", 'samples/randombox.r')

        # when
        mreq.services.enqueue_job(task, {"ret": 2, "rept": 1000}, "sequential")
        result = start_worker()

        # then
        self.assertEqual(result, 5)

    def test_r_slowfib(self):
        # given
        task = create_task("draft", 'samples/draft.r')

        # when
        mreq.services.enqueue_job(task, {}, "sequential")
        result = start_worker()

        # then
        self.assertEqual(result, 5)


class TasksApiTests(BaseTests):

    def setUp(self):
        super().setUp()
        self.app: FlaskClient = app.test_client()
        self.app.testing = True

    def test_get_tasks(self):
        # given
        draft = create_task("draft", 'samples/draft.r', [])
        randombox = create_task("randombox", 'samples/slow_fib.py')

        # when
        response = self.app.get("/tasks")

        # then
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        items = data["items"]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        items_without_excluded_keys = [without_keys(item, EXCLUDED_KEYS) for item in items]
        self.assertIn(without_keys(draft.raw_document, EXCLUDED_KEYS), items_without_excluded_keys)
        self.assertIn(without_keys(randombox.raw_document, EXCLUDED_KEYS), items_without_excluded_keys)

    def test_successful_create_task(self):
        # given
        form = {"data": json.dumps({FIELD_NAME: "draft", FIELD_PARAM_DEFINITIONS: []}),
                FIELD_SCRIPT_FILE: (BytesIO(b'print("draft")'), "draft.r"),
                FIELD_AUXILIAR_FILES: [(BytesIO(b'test1'), "test1.txt"),
                                       (BytesIO(b'test2'), "test2.txt")]}

        # when
        response = self.app.post("/tasks", data=form)

        # then
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        task = Task.find_one(data["_id"])
        self.assertIsNotNone(task)
        self.assertEqual(without_keys(data, EXCLUDED_KEYS), without_keys(task.raw_document, EXCLUDED_KEYS))
        self.assertTrue(os.path.exists(task.working_dir))
        self.assertTrue(os.path.exists(os.path.join(task.working_dir, )))

    @patch("mrq.job.queue_job")
    def test_successful_execute_task(self, mock_queue_job: MagicMock):
        # given
        task = create_task("draft", 'samples/draft.r', [])

        # when
        params = {"param1": 1, "param2": "2"}
        queue = "sequential"
        response = self.app.put("/tasks/%s" % str(task.id),
                                content_type="application/json",
                                data=json.dumps({FIELD_PARAMS: params, FIELD_QUEUE: queue}))

        # then
        self.assertEqual(response.status_code, 200)
        mock_queue_job.assert_called_once_with(R_TASK, {**task.params, **params}, queue=queue)



def without_keys(document, keys):
    return {x: document[x] for x in document if x not in keys}

def create_task(name: str, script_file_path: str, param_definitions=None):
    if param_definitions is None:
        param_definitions = []

    with open(script_file_path, 'rb') as script_file:
        script_file = FileStorage(script_file)
        task: Task = mreq.services.create_task(name, param_definitions, script_file, [])
    return task


def start_worker():
    if "GEVENT_RESOLVER" not in os.environ:
        os.environ["GEVENT_RESOLVER"] = "ares"
    from gevent import monkey
    monkey.patch_all(subprocess=False)
    cfg = config.get_config(file_path="workers/sequential.py", config_type="worker")
    worker_class = load_class_by_path(cfg["worker_class"])
    set_current_config(cfg)
    worker = worker_class()
    worker.max_jobs = 1
    return worker.work()


if __name__ == '__main__':
    unittest.main()