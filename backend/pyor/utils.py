import hashlib
import json

import datetime
import re
from copy import copy

from bson import ObjectId
from eve.io.mongo.mongo import Mongo
from flask import Response


class MongoJSONEncoder(json.JSONEncoder):

    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)

def jsonify(*args, **kwargs):
    """ jsonify with support for MongoDB ObjectId
    """
    return Response(
        json.dumps(
            dict(
                *args,
                **kwargs),
            cls=MongoJSONEncoder),
        mimetype='application/json')

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
    json_encoder = Mongo.json_encoder_class() # Fixed the JSON Encoder
    h.update(json.dumps(value_, sort_keys=True,
                        default=json_encoder.default).encode('utf-8'))
    return h.hexdigest()


def snake_case(name:str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()