import os

import importlib.util
import pathlib
import json
from logging import Logger
from typing import Dict

import rpy2.rinterface as ri
import rpy2.robjects as ro
from rpy2.robjects.vectors import ListVector

import celery
from celery.utils.log import get_task_logger

from pyor.celery import app
from pyor.celery.states import PROGRESS
from pyor.models import Experiment, Task, TaskFile, FileSource

__all__ = ["experiment_task"]

logger: Logger = get_task_logger(__name__)


class BaseTask(celery.Task):

    def update_progress(self, progress: float):
        if not isinstance(progress, float) or progress < 0.0 or progress > 1.0:
            logger.error("Tried to set progress to {}".format(progress))
            return
        self.update_state(state=PROGRESS, meta={"progress": progress})

@app.task(base=BaseTask, bind=True)
def experiment_task(self: BaseTask, id: str):
    experiment: Experiment = Experiment.objects.get(id=id)

    experiment_dir: str = os.path.join(experiment.task.dirpath, "experiments", str(experiment.id))
    logger.info("Creating experiment dir and changing workdir: {}".format(experiment_dir))
    pathlib.Path(experiment_dir).mkdir(parents=True, exist_ok=True)
    os.chdir(experiment_dir)

    script_path = _symlink_file_source(experiment.task.script_file.file, experiment_dir)
    logger.info("Symlink created: {}".format(script_path))
    for auxiliar_file in experiment.task.auxiliar_files:
        symlink_path = _symlink_file_source(auxiliar_file.file, experiment_dir)
        logger.info("Symlink created: {}".format(symlink_path))

    if script_path.lower().endswith(".py"):
        logger.info("Starting Python experiment...")
        return execute_python_script(self, script_path, experiment.params)
    else:
        logger.info("Starting R experiment...")
        return execute_r__script(self, script_path, experiment.params)

def execute_python_script(task: experiment_task, script_path: str, params: Dict):
    spec = importlib.util.spec_from_file_location('task_module', script_path)
    task_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(task_module)
    return task_module.run(task, params)

def execute_r__script(task: experiment_task, script_path: str, params: Dict):
    ro.globalenv['update_progress'] = ri.rternalize(task.update_progress)
    ro.globalenv['params'] = ListVector(params)

    with open(script_path, 'r') as script:
        ro.r(script.read())

def _symlink_file_source(file_source: FileSource, dir: str) -> str:
    new_filepath = os.path.join(dir, file_source.original_filename)
    os.symlink(file_source.filepath, new_filepath)
    return new_filepath