import os
import unittest

from mrq import config, context
from mrq.context import set_current_config
from mrq.utils import load_class_by_path
from pymongo.collection import Collection
from werkzeug.datastructures import FileStorage

import mreq
from mreq.models import Task
import mreq.services

import shutil

TEST_TASK = 'test_task'

context.setup_context(file_path="workers/mrqconfig.py")
collection: Collection = context.connections.mongodb_jobs.mreq_tasks

class TestTasksExecution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ["MREQ_DATA"] = os.path.join(os.environ["MREQ_DATA"], "tests")


    def setUp(self):
        os.chdir(os.environ["MREQ_BACKEND"])
        shutil.rmtree(os.path.join(os.environ["MREQ_DATA"], "tasks"), ignore_errors=True)
        collection.delete_one({"name": TEST_TASK})

    def test_python_slow_fib(self):
        with open('samples/slow_fib.py', 'rb') as fp:
            task = create_task(fp)
            mreq.services.enqueue_job(task.id, {"n": 30}, "sequential")

            result = start_worker()
            self.assertEqual(result, 5)

    def test_r_randombox(self):
        with open('samples/randombox.r', 'rb') as fp:
            task = create_task(fp)
            mreq.services.enqueue_job(task.id, {"ret": 2, "rept": 1000}, "sequential")

            result = start_worker()
            self.assertEqual(result, 5)

    def test_r_slowfib(self):
        with open('samples/draft.r', 'rb') as fp:
            task = create_task(fp)
            mreq.services.enqueue_job(task.id, {}, "sequential")

            result = start_worker()
            self.assertEqual(result, 5)



def create_task(fp):
    script_file = FileStorage(fp)
    task: Task = mreq.services.create_task(TEST_TASK, script_file, [])
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