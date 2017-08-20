import os

import pathlib
from typing import Union, List, Dict

from bson.objectid import ObjectId
from mrq import context
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult

# MRQ
context.setup_context(file_path="workers/mrqconfig.py")
collection: Collection = context.connections.mongodb_jobs.mreq_tasks

class Task(object):
    def __init__(self, name: Union[str, None] = None, script_name: Union[str, None] = None, id: Union[str, None] = None, document: Dict = None) -> None:
        if document:
            self.document = document
        else:
            if id is None:
                self.id = None
            else:
                self.id = ObjectId(id)

            self.name = name
            self.script_name = script_name

    @property
    def working_dir(self):
        return os.path.join(os.environ["MREQ_DATA"], "tasks", self.name)

    @property
    def script_path(self):
        return os.path.join(self.working_dir, self.script_name)

    @property
    def params(self):
        return {"task_name": self.name,
                "working_dir": self.working_dir,
                "script_path": self.script_path}

    @property
    def document(self):
        document = {"name": self.name, "script_name": self.script_name}
        if not self.id is None:
            document["_id"] = self.id
        return document

    @document.setter
    def document(self, document):
        self.id = document["_id"]
        self.name = document["name"]
        self.script_name = document["script_name"]

    def exists(self):
        """ Returns True if a job with the current _id exists in MongoDB. """
        return bool(collection.find_one({"name": self.name}, projection={"_id": 1}))

    @classmethod
    def insert(cls, task) -> bool:
        result: InsertOneResult = collection.insert_one(task.document)
        if result.inserted_id is None:
            return False
        task.id = result.inserted_id
        return True

    @classmethod
    def find_one(cls, id):
        document = collection.find_one(id)
        if document is None:
            return None
        return Task(document=document)

    @classmethod
    def find_all(cls) -> List:
        cursor: Cursor = collection.find()
        tasks = []
        for document in cursor:
            tasks.append(Task(document=document))
        return tasks

    def __repr__(self) -> str:
        return "<Task name=%s, script_name=%s>" % (self.name, self.script_name)
