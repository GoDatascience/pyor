import os
import sys
from multiprocessing import Process
from typing import Dict

from mrq import config
from mrq.context import set_current_config
from mrq.exceptions import StopRequested
from mrq.utils import load_class_by_path

WORKERS_DIR = "workers"


def start_workers():
    for worker_config_file in os.listdir(WORKERS_DIR):
        os.path.join(WORKERS_DIR, worker_config_file)


def start_workers_from_config(worker_config: str):
    cfg:Dict = config.get_config(file_path=worker_config)

    number_of_processes:int = cfg["processes"]
    if number_of_processes > 0:
        for i in range(number_of_processes):
            start_worker_process(worker_config)
    else:
        start_worker_process(worker_config)

def start_worker_process(worker_config):
    process = Process(target=start_worker, args=(worker_config))
    process.daemon = True
    process.start()


def start_worker(worker_config: str):
    if "GEVENT_RESOLVER" not in os.environ:
        os.environ["GEVENT_RESOLVER"] = "ares"

    from gevent import monkey
    monkey.patch_all(subprocess=False)

    cfg = config.get_config(file_path=worker_config)

    worker_class = load_class_by_path(cfg["worker_class"])
    set_current_config(cfg)

    w = worker_class()

    try:
        exitcode = w.work()
    except StopRequested:
        exitcode = 0

    sys.exit(exitcode)

if __name__ == "__main__":
    start_workers()