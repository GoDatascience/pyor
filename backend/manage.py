import subprocess

import multiprocessing

import os
from flask_script import Manager

from pyor.api import app
from pyor.models import Queue, Worker

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

def run_worker(worker: Worker):
    subprocess.Popen(worker.start_command.split(" "))

def run_flower():
    subprocess.Popen("celery flower -A pyor.celery --address=0.0.0.0 --port=5555".split(" "))


@manager.command
def runserver():
    createDefaultQueuesAndWorkers()

    for worker in Worker.objects:
        run_worker(worker)

    run_flower()

    # Flask
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT")))

if __name__ == "__main__":
    manager.run()