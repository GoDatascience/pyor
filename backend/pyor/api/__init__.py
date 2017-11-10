from eve import Eve
from eve.io.mongo.mongo import Mongo
from eve_swagger import swagger
from flask_cors.extension import CORS
from flask_login import current_user
from flask_mail import Mail
from flask_oauthlib.contrib.oauth2 import bind_cache_grant

from pyor.api.auth import security, oauth, BearerAuth, user_datastore
from pyor.api.auth_endpoints import auth_bp
from pyor.api.media import PyorMediaStorage
from pyor.models import Role, User, Queue, Worker, TaskFile, Task, Experiment, READ_ROLE_SCOPE, WRITE_ROLE_SCOPE,\
    READ_USER_SCOPE, WRITE_USER_SCOPE, READ_QUEUE_SCOPE, WRITE_QUEUE_SCOPE, READ_WORKER_SCOPE, WRITE_WORKER_SCOPE,\
    READ_TASKFILE_SCOPE, WRITE_TASKFILE_SCOPE, READ_TASK_SCOPE, WRITE_TASK_SCOPE, READ_EXPERIMENT_SCOPE,\
    WRITE_EXPERIMENT_SCOPE
from pyor.api.mapper import register_resource

from pyor.api.settings import SETTINGS

# Eve


class BlinkerCompatibleEve(Eve):
    """
    Workaround for https://github.com/pyeve/eve/issues/1087
    """
    def __getattr__(self, name):
        if name in {"im_self", "im_func"}:
            raise AttributeError("type object '%s' has no attribute '%s'" %
                                 (self.__class__.__name__, name))
        return super(BlinkerCompatibleEve, self).__getattr__(name)


app = BlinkerCompatibleEve(settings=SETTINGS, media=PyorMediaStorage, data=Mongo, auth=BearerAuth)
app.config['SECRET_KEY'] = 'super-secret' # TODO

register_resource({
    Role: {
        "url": "roles",
        "item_methods": ["GET", "DELETE"],
        "allowed_read_roles": [READ_ROLE_SCOPE],
        "allowed_write_roles": [WRITE_ROLE_SCOPE]
    },
    User: {
        "url": "users",
        "item_methods": ["GET", "DELETE"],
        "allowed_read_roles": [READ_USER_SCOPE],
        "allowed_write_roles": [WRITE_USER_SCOPE],
        "datasource": {"projection": {"password": 0}}
    },
    Queue: {
        "url": "queues",
        "allowed_read_roles": [READ_QUEUE_SCOPE],
        "allowed_write_roles": [WRITE_QUEUE_SCOPE]
    },
    Worker: {
        "url": "workers",
        "allowed_read_roles": [READ_WORKER_SCOPE],
        "allowed_write_roles": [WRITE_WORKER_SCOPE]
    },
    TaskFile: {
        "url": "taskfiles",
        "item_methods": ["GET", "DELETE"],
        "allowed_read_roles": [READ_TASKFILE_SCOPE],
        "allowed_write_roles": [WRITE_TASKFILE_SCOPE]
    },
    Task: {
        "url": "tasks",
        "versioning": True,
        "allowed_read_roles": [READ_TASK_SCOPE],
        "allowed_write_roles": [WRITE_TASK_SCOPE]
    },
    Experiment: {
        "url": "experiments",
        "item_methods": ["GET", "DELETE"],
        "allowed_read_roles": [READ_EXPERIMENT_SCOPE],
        "allowed_write_roles": [WRITE_EXPERIMENT_SCOPE]
    },
})

from pyor.api.hooks import *

# Swagger
app.register_blueprint(swagger)

# CORS
CORS(app)

# Mail
mail = Mail(app)

# Security
security.init_app(app, datastore=user_datastore)
oauth.init_app(app)
bind_cache_grant(app, oauth, current_user)
app.register_blueprint(auth_bp)
