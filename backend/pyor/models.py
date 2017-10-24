import os

from datetime import datetime

from mongoengine import *

class Queue(Document):
    name = StringField(required=True, unique=True)

class Worker(Document):
    name = StringField(required=True, unique=True)
    queues = ListField(ReferenceField(Queue))
    num_processes = IntField(min_value=1)

    @property
    def start_command(self):
        return "celery multi start {} -A pyor.celery --loglevel=INFO --events --concurrency={} --queues={} --pidfile={} --logfile={}"\
            .format(self.name, self.num_processes, ",".join([queue.name for queue in self.queues]), self.pidfile, self.logfile)

    @property
    def pidfile(self):
        return os.path.join(os.environ["PYOR_RUN"], "%n.pid")

    @property
    def logfile(self):
        return os.path.join(os.environ["PYOR_LOG"], "%n%I.log")

class ParamDefinition(EmbeddedDocument):
    name = StringField(required=True)
    type = StringField(required=True, choices=("text", "number", "date", "boolean"))

class Task(Document):
    name = StringField(required=True, unique=True)
    script_name = StringField(required=True)
    param_definitions = ListField(EmbeddedDocumentField(ParamDefinition))
    created = DateTimeField(default=datetime.now)

    @property
    def working_dir(self):
        return os.path.join(os.environ["PYOR_DATA"], "tasks", self.name)

    @property
    def script_path(self):
        return os.path.join(self.working_dir, self.script_name)

    @property
    def params(self):
        return {"task_name": self.name,
                "working_dir": self.working_dir,
                "script_path": self.script_path}