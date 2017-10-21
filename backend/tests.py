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
from werkzeug.datastructures import FileStorage

import pyor
from pyor import app
from pyor.controllers.tasks import FIELD_NAME, FIELD_PARAM_DEFINITIONS, FIELD_SCRIPT_FILE, FIELD_AUXILIAR_FILES, \
    FIELD_PARAMS, FIELD_QUEUE
from pyor.models import Task, Task
import pyor.services

import shutil

from pyor.services import R_TASK

context.setup_context(file_path="workers/mrqconfig.py")


class BaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["PYOR_DATA"] = os.path.join(os.environ["PYOR_DATA"], "tests")

    def setUp(self):
        os.chdir(os.environ["PYOR_BACKEND"])
        shutil.rmtree(os.path.join(os.environ["PYOR_DATA"], "tasks"), ignore_errors=True)
        Task.drop_collection()


class TasksExecutionTests(BaseTests):

    def test_python_slow_fib(self):
        # given
        task = create_task("slowbix", 'samples/slow_fib.py')

        # when
        pyor.services.enqueue_job(task, {"n": 20}, "sequential")
        result = start_worker()

        # then
        self.assertEqual(result, 5)

    def test_r_randombox(self):
        # given
        task = create_task("randombox", 'samples/randombox.r')

        # when
        pyor.services.enqueue_job(task, {"ret": 2, "rept": 1000}, "sequential")
        result = start_worker()

        # then
        self.assertEqual(result, 5)

    def test_r_draft(self):
        # given
        task = create_task("draft", 'samples/draft.r')

        # when
        pyor.services.enqueue_job(task, {}, "sequential")
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
        documents = [Task.from_json(json.dumps(item)) for item in items]
        self.assertIn(draft, documents)
        self.assertIn(randombox, documents)

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
        task = Task.objects(pk=data["_id"]).first()
        self.assertIsNotNone(task)
        self.assertEqual(Task.from_json(response.data), task)
        self.assertTrue(os.path.exists(task.working_dir))
        self.assertTrue(os.path.exists(os.path.join(task.working_dir, )))

    @patch("mrq.job.queue_job")
    def test_successful_execute_task(self, mock_queue_job: MagicMock):
        # given
        task = create_task("draft", 'samples/draft.r', [])

        # when
        params = {"param1": 1, "param2": "2"}
        queue = "sequential"
        response = self.app.put("/tasks/%s" % str(task.pk),
                                content_type="application/json",
                                data=json.dumps({FIELD_PARAMS: params, FIELD_QUEUE: queue}))

        # then
        self.assertEqual(response.status_code, 200)
        mock_queue_job.assert_called_once_with(R_TASK, {**task.params, **params}, queue=queue)


def create_task(name: str, script_file_path: str, param_definitions=None):
    if param_definitions is None:
        param_definitions = []

    with open(script_file_path, 'rb') as script_file:
        script_file = FileStorage(script_file)
        task: Task = pyor.services.create_task(name, param_definitions, script_file, [])
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