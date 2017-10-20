import importlib.util

from pyor.tasks.base import BaseTask


def run_python_script(script_path, params):
    spec = importlib.util.spec_from_file_location('task', script_path)
    task = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(task)
    task.run(params)

class PythonTask(BaseTask):

    def run(self, params):
        run_python_script(self.script_path, params)