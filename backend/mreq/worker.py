import os
import sys
from typing import List

from mrq import config
from mrq.context import set_current_config
from mrq.utils import load_class_by_path
from multiprocessing import Process


def start_worker(name: str, queues: List[str]):
    if "GEVENT_RESOLVER" not in os.environ:
        os.environ["GEVENT_RESOLVER"] = "ares"

    from gevent import monkey
    monkey.patch_all(subprocess=False)

    cfg = config.get_config(config_type="worker")
    cfg["name"] = name
    cfg["queues"] = queues

    worker_class = load_class_by_path(cfg["worker_class"])
    set_current_config(cfg)

    w = worker_class()

    exitcode = w.work()

    sys.exit(exitcode)


def start_workers_in_new_process(name: str, number_of_workers=1, *queues: str):
    for i in range(number_of_workers):
        process = Process(target=start_worker, args=("%s:%d" % (name, i), queues))
        process.daemon=True
        process.start()