import os

import importlib.util
import pathlib
import json
from typing import Dict

import rpy2.rinterface as ri
import rpy2.robjects as ro
from rpy2.robjects.vectors import ListVector

import celery
from celery.utils.log import get_task_logger

from pyor.celery import app

logger = get_task_logger(__name__)


class BaseTask(celery.Task):

    track_started = True

    def setup(self, working_dir: str, script_path: str, params: Dict):
        logger.info("Setting script_path: %s" % (script_path))

        params["output_dir"] = os.path.join(working_dir, str(self.request.id))
        logger.info("Creating output_dir: %s" % (params["output_dir"]))
        pathlib.Path(params["output_dir"]).mkdir(parents=True, exist_ok=True)

        params_file_path = os.path.join(params["output_dir"], "params.json")
        logger.info("Saving params.json: %s" % (params_file_path))
        with open(params_file_path, 'x') as params_file:
            json.dump(params, params_file)

        os.chdir(working_dir)

        logger.info("Running task...")

    def update_progress(self, progress: float):
        self.update_state(state="PROGRESS", meta={progress: progress})


@app.task(base=BaseTask, bind=True)
def python_task(self, working_dir: str, script_path: str, params: Dict):
    self.setup(working_dir, script_path, params)

    spec = importlib.util.spec_from_file_location('task', script_path)
    task = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(task)
    return task.run(self, params)

@app.task(base=BaseTask, bind=True)
def r_task(self, working_dir: str, script_path: str, params: Dict):
    self.setup(working_dir, script_path, params)

    ro.globalenv['update_progress'] = ri.rternalize(self.update_progress)
    ro.globalenv['params'] = ListVector(params)

    with open(script_path, 'r') as script:
        ro.r(script.read())