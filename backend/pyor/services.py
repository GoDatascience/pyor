import pathlib
from typing import List, Dict, Union

import os
import mrq.job
from werkzeug.datastructures import FileStorage

from pyor.exceptions import TaskNameAlreadyExists
from pyor.models import Task

R_TASK = "pyor.tasks.r.RTask"

PYTHON_TASK = "pyor.tasks.python.PythonTask"


def create_task(name: str, param_definitions: List[Dict], script_file: FileStorage,
                auxiliar_files: List[FileStorage]) -> Union[Task, None]:
    task = Task(name=name, script_name=os.path.basename(script_file.filename), param_definitions=param_definitions)
    if task.this_exists():
        raise TaskNameAlreadyExists()
    pathlib.Path(task.working_dir).mkdir(parents=True, exist_ok=True)
    if Task.insert(task):
        script_file.save(task.script_path)
        for auxiliar_file in auxiliar_files:
            auxiliar_file.save(os.path.join(task.working_dir, auxiliar_file.filename))
        return task
    else:
        return None


def enqueue_job(task: Task, params: Dict, queue: str):
    params = {**task.params, **params}
    mrq.job.queue_job(PYTHON_TASK if ".py" in task.script_name else R_TASK,
                      params, queue=queue)
