import pathlib
from typing import List, Dict, Union

import os
from werkzeug.datastructures import FileStorage

from pyor.models import Task, ParamDefinition
from pyor.tasks import python_task, r_task


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


def enqueue_job(task: Task, params: Dict, queue: str):
    celery_task = python_task if ".py" in task.script_name else r_task
    celery_task.apply_async((task.working_dir, task.script_path, params), shadow=task.name, queue=queue)
