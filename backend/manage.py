import subprocess

import multiprocessing

import os
from datetime import datetime

from flask_script import Manager

from pyor.api import app
from pyor.api.auth import user_datastore
from pyor.models import Queue, Worker, Role, User, Client, IMPLICIT_GRANT, ADMIN_SCOPES,\
    SCIENTIST_SCOPES, ADMIN_ROLE, SCIENTIST_ROLE
from pyor.models.constants import ALL_SCOPES

manager = Manager(app)

def createDefaultQueuesAndWorkers():
    queues = Queue.objects
    if not queues:
        sequential_queue = Queue(name="sequential")
        sequential_queue.save()
        parallel_queue = Queue(name="parallel")
        parallel_queue.save()

        sequential_worker = Worker(name="sequential", queues=[sequential_queue], num_processes=1)
        sequential_worker.save()

        parallel_worker = Worker(name="parallel", queues=[parallel_queue], num_processes=multiprocessing.cpu_count())
        parallel_worker.save()


def createDefaultUsersAndRoles():
    if not User.objects:
        admin_role: Role = user_datastore.find_or_create_role(name=ADMIN_ROLE,
                                                              description="Administrator of the system",
                                                              allowed_scopes=ADMIN_SCOPES)
        user_datastore.find_or_create_role(name=SCIENTIST_ROLE,
                                           description="Regular user",
                                           allowed_scopes=SCIENTIST_SCOPES)
        user_datastore.create_user(email='admin', password='admin', roles=[admin_role], confirmed_at=datetime.utcnow())


def createDefaultClients():
    if not Client.objects:
        Client(name="Frontend", client_id="frontend", redirect_uris=[os.environ["FRONTEND_URL"],
                                                                     "http://localhost:3200/oauth2-redirect.html"],
               default_scopes=ALL_SCOPES, allowed_grant_types=[IMPLICIT_GRANT]).save()


def run_worker(worker: Worker):
    subprocess.Popen(worker.start_command.split(" "))


def run_flower():
    subprocess.Popen("celery flower -A pyor.celery --address=0.0.0.0 --port=5555".split(" "))


@manager.command
def runserver():
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        createDefaultQueuesAndWorkers()
        createDefaultUsersAndRoles()
        createDefaultClients()

        for worker in Worker.objects:
            run_worker(worker)

        run_flower()

    # Flask
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT")))


if __name__ == "__main__":
    manager.run()