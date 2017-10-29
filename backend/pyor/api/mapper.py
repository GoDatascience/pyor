from datetime import datetime
from typing import Type, Dict

from mongoengine import DateTimeField
from mongoengine.document import Document

from pyor.api.schema import SchemaMapper
from pyor.models import LAST_UPDATED, DATE_CREATED, ETAG, patch_model_class
from pyor.utils import snake_case

schemaMapper = SchemaMapper()


def register_resource(registrations: Dict[Type[Document], Dict], lowercase=True):
    for model_cls, settings in registrations.items():
        if not issubclass(model_cls, Document):
            raise TypeError("Class '%s' is not a subclass of "
                            "mongoengine.Document." % model_cls.__name__)

        if settings is None:
            settings = {}

        resource_name = model_cls.__name__
        if lowercase:
            resource_name = resource_name.lower()

        if "source" not in settings:
            settings["datasource"] = {"source": snake_case(model_cls.__name__)}

        patch_model_class(model_cls)
        settings["schema"] = schemaMapper.create_schema(model_cls, lowercase)

        app().register_resource(resource_name, settings)

        for subresource_model_settings in schemaMapper.get_subresource_settings(model_cls, resource_name,
                                                                  settings, registrations, lowercase):
            app().register_resource(*subresource_model_settings)


def app():
    from pyor.api import app
    return app

