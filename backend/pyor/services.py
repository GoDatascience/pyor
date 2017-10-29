import os
import pathlib
from datetime import datetime
from typing import List, Dict

from kombu import uuid
from werkzeug.datastructures import FileStorage

from pyor.celery.states import PENDING
from pyor.celery.tasks import python_task, r_task
from pyor.models import Task, ParamDefinition, Experiment, Queue


def create_task(name: str, param_definitions: List[Dict], script_file: FileStorage,
                auxiliar_files: List[FileStorage]) -> Task:
    param_definitions: List[ParamDefinition] = [ParamDefinition(**param_definition) for param_definition in param_definitions]
    task = Task(name=name, script_name=os.path.basename(script_file.filename), param_definitions=param_definitions)

    pathlib.Path(task.working_dir).mkdir(parents=True, exist_ok=True)
    task.save()
    script_file.save(task.script_path)
    for auxiliar_file in auxiliar_files:
        auxiliar_file.save(os.path.join(task.working_dir, auxiliar_file.filename))
    return task


def enqueue_experiment(task: Task, params: Dict, queue: Queue):
    experiment = Experiment(task=task, date_received=datetime.utcnow(), params=params, queue=queue).save()

    celery_task = python_task if ".py" in task.script_name else r_task
    celery_task.apply_async((task.working_dir, task.script_path, params), task_id=str(experiment.id), task=task, shadow=task.name, queue=queue.name)
