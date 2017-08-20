#!/usr/bin/env python

import os
from typing import Dict

from mrq import config

WORKERS_DIR = "workers"
SUPERVISORD_CONF = "supervisord.conf"

IGNORED_FILES = ("__init__.py", "mrqconfig.py")

def append_workers():
    with open(SUPERVISORD_CONF) as supervisor_file:
        supervisor_content = [supervisor_file.read()]
        filenames = [filename for filename in os.listdir(WORKERS_DIR) if
                  ".py" in filename and not filename in IGNORED_FILES]
        for worker_config_name in filenames:
            worker_config_path = os.path.join(WORKERS_DIR, worker_config_name)
            cfg: Dict = config.get_config(file_path=worker_config_path)
            name: str = cfg["name"] if "name" in cfg else worker_config_name.replace(".py", "")
            number_of_processes: int = cfg["processes"] if "processes" in cfg else 1
            supervisor_content.append("""
            
[program:mreq-worker-%s]
directory=/opt/mreq/backend
command=mrq-worker --config=%s
process_name=mreqworker-%s-%%(process_num)s
numprocs=%d
startsecs=1
startretries=3
stopsignal=TERM
autostart=true
autorestart=unexpected
exitcodes=0,2,3
stopasgroup=false
killasgroup=false""" % (name, worker_config_path, name, number_of_processes))
        return "".join(supervisor_content)


if __name__ == "__main__":
    print(append_workers())