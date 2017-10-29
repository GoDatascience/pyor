from datetime import datetime, timedelta


from celery.backends.base import BaseBackend
from pyor.celery.states import PENDING, READY_STATES, RETRY, STARTED
from kombu.utils import cached_property

from pyor.models import Experiment


class PyorBackend(BaseBackend):

    def __init__(self, app=None, **kwargs):
        super(PyorBackend, self).__init__(app, **kwargs)

    def _store_result(self, task_id, result, state,
                      traceback=None, request=None, **kwargs):
        """Store return value and state of an executed task."""
        experiment = Experiment.objects.get(id=task_id)

        if experiment:
            experiment.status = state
            if state == STARTED:
                experiment.date_started = datetime.utcnow()
            if state in READY_STATES:
                experiment.date_done = datetime.utcnow()
            if state == RETRY:
                experiment.retry_count += 1
            experiment.date_last_update = datetime.utcnow()
            experiment.result = result
            experiment.traceback = traceback
            experiment.children = self.current_task_children(request)

            if isinstance(result, dict) and "progress" in result:
               experiment.progress = result["progress"]

            experiment.save()

        return result

    def _get_task_meta_for(self, task_id):
        """Get task meta-data for a task by id."""
        experiment = Experiment.objects.get(id=task_id)

        if not experiment:
            return {'status': PENDING, 'result': None}

        return self.meta_from_decoded({
            'task_id': task_id,
            'status': experiment.status,
            'result': experiment.result,
            'traceback': experiment.traceback,
            'children': experiment.children,
        })

    def _forget(self, task_id):
        """Remove result."""
        experiment = Experiment.objects.get(id=task_id)
        if experiment:
            experiment.delete()

    def cleanup(self):
        """Delete expired meta-data."""
        if self.expires_delta:
            for experiment in Experiment.objects(date_done__lt= self.app.now() - self.expires_delta):
                experiment.delete()

    @cached_property
    def expires_delta(self):
        if not self.expires:
            return None
        return timedelta(seconds=self.expires)

    def _save_group(self, group_id, result):
        """Save the group result."""
        raise NotImplementedError("Group operations aren't supported")

    def _restore_group(self, group_id):
        """Get the result for a group by id."""
        raise NotImplementedError("Group operations aren't supported")

    def _delete_group(self, group_id):
        """Delete a group by id."""
        raise NotImplementedError("Group operations aren't supported")
