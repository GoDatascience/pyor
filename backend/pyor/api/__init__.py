from eve import Eve
from eve.io.mongo.mongo import Mongo
from eve_swagger import swagger, add_documentation
from flask_cors.extension import CORS

from pyor.api.media import PyorMediaStorage
from pyor.models import Queue, Worker, TaskFile, Task, Experiment
from pyor.api.mapper import register_resource

from pyor.api.settings import SETTINGS


app = Eve(settings=SETTINGS, media=PyorMediaStorage, data=Mongo)
app.register_blueprint(swagger)
CORS(app)

register_resource({Queue: {"url": "queues"},
                   Worker: {"url": "workers"},
                   TaskFile: {
                       "url": "taskfiles",
                       "item_methods": ["GET", "DELETE"]
                   },
                   Task: {"url": "tasks"},
                   Experiment: {
                       "url": "experiments",
                       "item_methods": ["GET", "DELETE"]
                   }})

from pyor.api.hooks import *