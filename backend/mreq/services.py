import pathlib
from typing import List, Dict, Union

import os
from mrq import job
from werkzeug.datastructures import FileStorage

from mreq.exceptions import TaskNameAlreadyExists
from mreq.models import Task


def create_task(name: str, script_file: FileStorage, auxiliar_files: List[FileStorage]) -> Union[Task, None]:
    task = Task(name, os.path.basename(script_file.filename))
    if task.exists():
        raise TaskNameAlreadyExists()
    pathlib.Path(task.working_dir).mkdir(parents=True, exist_ok=True)
    if Task.insert(task):
        script_file.save(task.script_path)
        for auxiliar_file in auxiliar_files:
            auxiliar_file.save(task.working_dir)
        return task
    else:
        return None


def enqueue_job(task_id: str, params: Dict, queue: str):
    task = Task.find_one(task_id)
    if not task is None:
        params = {**task.params, **params}
        job.queue_job("mreq.tasks.python.PythonTask" if ".py" in task.script_name else "mreq.tasks.r.RTask",
                      params, queue=queue)

