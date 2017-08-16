from mrq import context
from mrq.job import Job
from mrq.task import Task

import rpy2.rinterface as ri
import rpy2.robjects as ro

from mreq.tasks.base import BaseTask


def run_r_script(script_path, params):
    with open(script_path, 'r') as script:
        ro.r(script)

class RTask(BaseTask):
    def run(self, params):
        job: Job = context.get_current_job()
        ro.globalenv['set_progress'] = ri.rternalize(job.set_progress)
        ro.globalenv['params'] = params
