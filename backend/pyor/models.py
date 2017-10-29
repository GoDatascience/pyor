import os

from datetime import datetime

from pyor.celery.states import PENDING
from mongoengine import *

connect(os.environ["MONGO_DBNAME"], host=os.environ["MONGO_HOST"], port=int(os.environ["MONGO_PORT"]))

LAST_UPDATED = "_updated"
DATE_CREATED = "_created"

class FileSource(Document):
    filename = StringField(required=True)
    original_filename = StringField()
    filepath = StringField(required=True)
    length = LongField(required=True, min_value=0)
    md5 = StringField()
    content_type = StringField()
    upload_date = DateTimeField(default=datetime.utcnow)

    meta = {'allow_inheritance': True}


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


class TaskFiles(Document):
    script_file = ReferenceField(FileSource)
    auxiliar_files = ListField(ReferenceField(FileSource))


class Task(Document):
    name = StringField(required=True, unique=True)
    files = ReferenceField(TaskFiles, db_field="files_id")
    param_definitions = ListField(EmbeddedDocumentField(ParamDefinition))

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


class Experiment(Document):
    task = ReferenceField(Task, required=True, db_field="task_id")
    params = DictField()
    queue = ReferenceField(Queue, required=True, db_field="queue_id")
    status = StringField(required=True, default=PENDING, api_readonly=True)
    result = DynamicField(api_readonly=True)
    result_files = ListField(ReferenceField(FileSource), api_readonly=True)
    retry_count = IntField(default=0, api_readonly=True)
    date_received = DateTimeField(api_readonly=True)
    date_started = DateTimeField(api_readonly=True)
    date_last_update = DateTimeField(api_readonly=True)
    date_done = DateTimeField(api_readonly=True)
    traceback = StringField(api_readonly=True)
    children = DynamicField(api_readonly=True)
    progress = FloatField(min_value=0.0, max_value=1.0, api_readonly=True)