import os

import pathlib
from mrq import context
from mrq.context import log
from mrq.job import Job
from mrq.task import Task
import json

class BaseTask(Task):

    def __init__(self):
        super().__init__()
        self.script_path = None
        self.job = None

    def run_wrapped(self, params):
        working_dir = params["working_dir"]
        script_path = params["script_path"]

        if not working_dir or not script_path:
            raise ValueError("'working_dir' and 'script_path' are required!")

        log.info("Setting script_path: %s" % (script_path))
        self.script_path = script_path
        self.job: Job = context.get_current_job()

        params["output_dir"] = os.path.join(params["working_dir"], str(self.job.id))
        log.info("Creating output_dir: %s" % (params["output_dir"]))
        pathlib.Path(params["output_dir"]).mkdir(parents=True, exist_ok=True)

        params_file_path = os.path.join(params["output_dir"], "params.json")
        log.info("Saving params.json: %s" % (params_file_path))
        with open(params_file_path, 'x') as params_file:
            json.dump(params, params_file)

        os.chdir(working_dir)

        log.info("Running task...")
        self.run(params)

        return params["output_dir"]