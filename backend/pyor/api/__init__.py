from eve import Eve
from eve_swagger import swagger, add_documentation
from flask_cors.extension import CORS

from pyor.api.media import PyorMediaStorage
from pyor.models import Queue, Worker, TaskFiles, Task, Job
from pyor.api.mapper import register_resource

from pyor.api.settings import SETTINGS


app = Eve(settings=SETTINGS, media=PyorMediaStorage)
app.register_blueprint(swagger)
CORS(app)

register_resource({Queue: {"url": "queues"},
                   Worker: {"url": "workers"},
                   TaskFiles: {
                       "url": "taskfiles",
                       "item_methods": ["GET", "DELETE"]
                   },
                   Task: {"url": "tasks"},
                   Job: {
                       "url": "jobs",
                       "item_methods": ["GET", "DELETE"]
                   }})

from pyor.api.hooks import *