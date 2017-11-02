import json
from typing import Type, Dict, Union
from datetime import datetime

from bson import DBRef
from mongoengine import *
import hashlib
from copy import copy
from eve.io.mongo.mongo import Mongo
from mongoengine.connection import get_db

from pyor.models.constants import *


class VersionedReferenceField(ReferenceField):
    def _get_versioned_document_dbref(self, value: Union[dict, Document], cls=None):
        if cls is None:
            cls = self.document_type

        collection = cls._get_collection_name() + VERSIONS
        id = get_db()[collection].find_one({ID_FIELD + VERSION_ID_SUFFIX: value[ID_FIELD], VERSION: value[VERSION]},
                                           {ID_FIELD: 1})[ID_FIELD]
        return DBRef(collection, id)

    def to_python(self, value: Dict):
        """Convert a MongoDB-compatible type to a Python type."""

        if (not self.dbref and isinstance(value, dict) and ID_FIELD in value and
                not isinstance(value[ID_FIELD], (DBRef, Document, EmbeddedDocument))):
            value = self._get_versioned_document_dbref(value)
        return value

    def to_mongo(self, document):
        if isinstance(document, DBRef):
            if not self.dbref:
                return get_db()[document.collection].find_one({ID_FIELD: document.id}, {ID_FIELD: 1, VERSION: 1})
            return document

        if isinstance(document, Document):
            # We need the id from the saved object to create the DBRef
            id = document.pk
            version = document[VERSION]
            if id is None:
                self.error('You can only reference documents once they have'
                           ' been saved to the database')

            # Use the attributes from the document instance, so that they
            # override the attributes of this field's document type
            cls = document
        else:
            raise TypeError()
            # id = document
            # cls = self.document_type

        id_field_name = cls._meta['id_field']
        id_field = cls._fields[id_field_name]

        id = id_field.to_mongo(id)
        if self.document_type._meta.get('abstract'):
            raise NotImplementedError()
        elif self.dbref:
            return self._get_versioned_document_dbref(document, cls)

        return {ID_FIELD: id, VERSION: version}

    def validate(self, value):
        if not isinstance(value, (self.document_type, DBRef, dict)):
            self.error('A VersionedReferenceField only accepts DBRef, dict or documents')

        if isinstance(value, Document) and value.id is None:
            self.error('You can only reference documents once they have been '
                       'saved to the database')

        if self.document_type._meta.get('abstract') and \
                not isinstance(value, self.document_type):
            self.error(
                '%s is not an instance of abstract reference type %s' % (
                    self.document_type._class_name)
            )


def last_updated_hook(sender: Type[Document], document: Document, **kwargs):
    """
    Hook which updates LAST_UPDATED field before every Document.save() call.
    """

    field_name = LAST_UPDATED.lstrip('_')
    if field_name in document._fields:
        document[field_name] = datetime.utcnow()


def etag_hook(sender: Type[Document], document: Document, **kwargs):
    """
    Hook which updates ETAG field before every Document.save() call.
    """

    field_name = ETAG.lstrip('_')
    if field_name in document._fields:
        etag = document_etag(document.to_mongo(), ignore_fields=["_SON__keys"])
        document[field_name] = etag


def patch_model_class(model_cls: Type[Document]):
    """
    Internal method invoked during registering new model.

    Adds necessary fields (updated, created and etag) into model class
    to ensure Eve's default functionality.

    This is a helper for correct manipulation with mongoengine documents
    within Eve. Eve needs 'updated' and 'created' fields for it's own
    purpose, but we cannot ensure that they are present in the model
    class. And even if they are, they may be of other field type or
    missbehave.

    :param model_cls: mongoengine's model class (instance of subclass of
                      :class:`mongoengine.Document`) to be fixed up.
    """

    # field names have to be non-prefixed
    last_updated_field_name = LAST_UPDATED.lstrip('_')
    date_created_field_name = DATE_CREATED.lstrip('_')
    etag_field_name = ETAG.lstrip('_')

    new_fields = {
        last_updated_field_name: DateTimeField(db_field=LAST_UPDATED,
                                               default=datetime.utcnow),
        date_created_field_name: DateTimeField(db_field=DATE_CREATED,
                                               default=datetime.utcnow),
        etag_field_name: StringField(db_field=ETAG)
    }

    for attr_name, attr_value in new_fields.items():
        # If the field does exist, we just check if it has right
        # type (mongoengine.DateTimeField) and pass
        if attr_name in model_cls._fields:
            attr_value = model_cls._fields[attr_name]
            if not isinstance(attr_value, type(attr_value)):
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


# Copied from eve.utils because the worker process doesn't have the eve running
def document_etag(value, ignore_fields=None):
    """ Computes and returns a valid ETag for the input value.

    :param value: the value to compute the ETag with.
    :param ignore_fields: `ignore_fields` list of fields to skip to
                          compute the ETag value.

    .. versionchanged:: 0.5.4
       Use json_encoder_class. See #624.

    .. versionchanged:: 0.0.4
       Using bson.json_util.dumps over str(value) to make etag computation
       consistent between different runs and/or server instances (#16).
    """
    if ignore_fields:
        def filter_ignore_fields(d, fields):
            # recursive function to remove the fields that they are in d,
            # field is a list of fields to skip or dotted fields to look up
            # to nested keys such as  ["foo", "dict.bar", "dict.joe"]
            for field in fields:
                key, _, value = field.partition(".")
                if value:
                    filter_ignore_fields(d[key], [value])
                elif field in d:
                    d.pop(field)
                else:
                    # not required fields can be not present
                    pass

        value_ = copy(value)
        filter_ignore_fields(value_, ignore_fields)
    else:
        value_ = value

    h = hashlib.sha1()
    json_encoder = Mongo.json_encoder_class()  # Fixed the JSON Encoder
    h.update(json.dumps(value_, sort_keys=True,
                        default=json_encoder.default).encode('utf-8'))
    return h.hexdigest()
