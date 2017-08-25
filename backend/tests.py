import os
import unittest
from typing import IO, List

from io import FileIO

from flask.testing import FlaskClient
from mrq import config, context
from mrq.context import set_current_config
from mrq.utils import load_class_by_path
from pymongo.collection import Collection
from pymongo.database import Database
from werkzeug.datastructures import FileStorage

import mreq
from mreq import app
from mreq.models import Task
import mreq.services

import shutil

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
        mreq.services.enqueue_job(task, {"n": 30}, "sequential")
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
        draft = create_task("draft", 'samples/draft.r')
        randombox = create_task("randombox", 'samples/slow_fib.py')

        # when
        response = self.app.get("/tasks")

        # then
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)
        self.assertIn(draft.document, response.data)
        self.assertIn(randombox.document, response.data)



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