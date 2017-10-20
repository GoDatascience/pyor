import rpy2.rinterface as ri
import rpy2.robjects as ro
from rpy2.robjects import conversion
from rpy2.robjects.vectors import ListVector

from pyor.tasks.base import BaseTask


def run_r_script(script_path):
    with open(script_path, 'r') as script:
        ro.r(script.read())

class RTask(BaseTask):
    def run(self, params):
        ro.globalenv['set_progress'] = ri.rternalize(self.job.set_progress)
        ro.globalenv['params'] = ListVector(params)

        run_r_script(self.script_path)
