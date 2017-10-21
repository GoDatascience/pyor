import os

from datetime import datetime

from mongoengine import *

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