import mongoengine

from pyor.models.constants import *
from pyor.models.entities import *
from pyor.models.eve_support import *

connect(os.environ["MONGO_DBNAME"], host=os.environ["MONGO_HOST"], port=int(os.environ["MONGO_PORT"]))

# Needed because the worker process doesn't call the pyor.api.mapper.register_resource()
patch_model_class(Role)
patch_model_class(User)
patch_model_class(Client)
patch_model_class(Queue)
patch_model_class(Worker)
patch_model_class(TaskFile)
patch_model_class(Task)
patch_model_class(Experiment)

mongoengine.signals.pre_save.connect(last_updated_hook)
mongoengine.signals.pre_save.connect(etag_hook)