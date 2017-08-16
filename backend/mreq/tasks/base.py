import os

from mrq.task import Task


class BaseTask(Task):

    def __init__(self):
        super().__init__()
        self.script_path = None

    def run_wrapped(self, params):
        working_dir = params['working_dir']
        script_path = params['script_path']

        if not working_dir or not script_path:
            raise ValueError("'working_dir' and 'script_path' are required!")

        os.chdir(working_dir)
        self.script_path = script_path
        return self.run(params)