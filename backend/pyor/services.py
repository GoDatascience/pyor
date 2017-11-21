import bcrypt

from pyor.celery.tasks import experiment_task
from pyor.models import Experiment, User


def insert_user(username:str, password:str):
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    User(username=username, password=hash).save()


def enqueue_experiment(id: str):
    experiment = Experiment.objects.get(id=id)
    args:tuple = (str(id),)
    experiment_task.apply_async(args, task_id=str(experiment.id), task=experiment.task,
                                shadow=experiment.task.name, queue=experiment.queue.name)