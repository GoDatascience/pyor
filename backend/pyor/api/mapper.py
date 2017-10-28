from datetime import datetime
from typing import Type, Dict, Union, List, Tuple

import mongoengine
from mongoengine import DateTimeField
from mongoengine.document import Document

from pyor.api.schema import SchemaMapper
from pyor.models import LAST_UPDATED, DATE_CREATED

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

        fix_model_class(model_cls)
        settings["schema"] = schemaMapper.create_schema(model_cls, lowercase)

        app().register_resource(resource_name, settings)

        for subresource_model_settings in schemaMapper.get_subresource_settings(model_cls, resource_name,
                                                                  settings, registrations, lowercase):
            app().register_resource(*subresource_model_settings)


def fix_model_class(model_cls: Type[Document]):
    """
    Internal method invoked during registering new model.

    Adds necessary fields (updated and created) into model class
    to ensure Eve's default functionality.

    This is a helper for correct manipulation with mongoengine documents
    within Eve. Eve needs 'updated' and 'created' fields for it's own
    purpose, but we cannot ensure that they are present in the model
    class. And even if they are, they may be of other field type or
    missbehave.

    :param model_cls: mongoengine's model class (instance of subclass of
                      :class:`mongoengine.Document`) to be fixed up.
    """
    date_field_cls = DateTimeField

    # field names have to be non-prefixed


    last_updated_field_name = LAST_UPDATED.lstrip('_')
    date_created_field_name = DATE_CREATED.lstrip('_')

    new_fields = {
        last_updated_field_name: date_field_cls(db_field=LAST_UPDATED,
                                                default=datetime.utcnow),
        date_created_field_name: date_field_cls(db_field=DATE_CREATED,
                                                default=datetime.utcnow)
    }

    for attr_name, attr_value in new_fields.items():
        # If the field does exist, we just check if it has right
        # type (mongoengine.DateTimeField) and pass
        if attr_name in model_cls._fields:
            attr_value = model_cls._fields[attr_name]
            if not isinstance(attr_value, DateTimeField):
                info = (attr_name, attr_value.__class__.__name__)
                raise TypeError("Field '%s' is needed by Eve, but has"
                                " wrong type '%s'." % info)
            continue
        # The way how we introduce new fields into model class is copied
        # out of mongoengine.base.DocumentMetaclass
        attr_value.name = attr_name
        if not attr_value.db_field:
            attr_value.db_field = attr_name
        # TODO: reverse-delete rules
        attr_value.owner_document = model_cls

        # now add a flag that this is automagically added field - it is
        # very useful when registering class more than once - create_schema
        # has to know, if it is user-added or auto-added field.
        attr_value.eve_field = True

        # now simulate DocumentMetaclass: add class attributes
        setattr(model_cls, attr_name, attr_value)
        model_cls._fields[attr_name] = attr_value
        model_cls._db_field_map[attr_name] = attr_value.db_field
        model_cls._reverse_db_field_map[attr_value.db_field] = attr_name

        # this is just copied from mongoengine and frankly, i just dont
        # have a clue, what it does...
        created = [(v.creation_counter, v.name) for v in model_cls._fields.values()]
        model_cls._fields_ordered = tuple(i[1] for i in sorted(created))

    mongoengine.signals.pre_save.connect(last_updated_hook, sender=model_cls)

def last_updated_hook(sender, document, **kwargs):
    """
    Hook which updates LAST_UPDATED field before every Document.save() call.
    """

    field_name = LAST_UPDATED.lstrip('_')
    if field_name in document:
        document[field_name] = datetime.utcnow()

def app():
    from pyor.api import app
    return app

