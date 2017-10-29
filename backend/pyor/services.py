from pyor.celery.tasks import experiment_task
from pyor.models import Experiment


def enqueue_experiment(id: str):
    experiment = Experiment.objects.get(id=id)
    args:tuple = (str(id),)
    experiment_task.apply_async(args, task_id=str(experiment.id), task=experiment.task,
                                shadow=experiment.task.name, queue=experiment.queue.name)