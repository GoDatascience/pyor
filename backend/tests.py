import os

from mrq import config, context
from mrq.context import set_current_config
from mrq.utils import load_class_by_path
from pymongo.collection import Collection
from werkzeug.datastructures import FileStorage

import mreq
from mreq.models import Task
import mreq.services

import shutil

context.setup_context(file_path="workers/mrqconfig.py")
collection: Collection = context.connections.mongodb_jobs.mreq_tasks

def cleanup():
    shutil.rmtree(os.path.join(os.environ["MREQ_DATA"], "tasks"), ignore_errors=True)
    collection.drop()


def create_task(fp):
    script_file = FileStorage(fp)
    task: Task = mreq.services.create_task('sample_python_task', script_file, [])
    return task


def test_python_task():
    with open('samples/sample_python_task.py', 'rb') as fp:
        task = create_task(fp)
        mreq.services.enqueue_job(task.id, {"n": 50}, "sequential")

        result = start_worker()
        assert result == 5


def test_r_task():
    with open('samples/sample_r_task.r', 'rb') as fp:
        script_file = FileStorage(fp)
        task: Task = mreq.services.create_task('sample_r_task', script_file, [])
        mreq.services.enqueue_job(task.id, {"ret": 2, "rept": 10000}, "sequential")

        result = start_worker()
        assert result == 5

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
    cleanup()
    # test_python_task()
    test_r_task()