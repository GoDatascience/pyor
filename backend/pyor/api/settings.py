import os

from pyor.models import LAST_UPDATED, DATE_CREATED, ETAG, VERSION, LATEST_VERSION

SETTINGS = {
    "DEBUG": True if os.environ.get("ENV") == "development" else False,
    "MONGO_HOST": os.environ["MONGO_HOST"],
    "MONGO_PORT": int(os.environ["MONGO_PORT"]),
    "MONGO_DBNAME": os.environ["MONGO_DBNAME"],

    "URL_PREFIX": "api",

    "PAGINATION_DEFAULT": 10,

    "LAST_UPDATED": LAST_UPDATED,
    "DATE_CREATED": DATE_CREATED,
    "ETAG": ETAG,
    "VERSION": VERSION,
    "LATEST_VERSION": LATEST_VERSION,
    "DATE_FORMAT": "%Y-%m-%dT%H:%M:%S.%fZ",

    "RESOURCE_METHODS": ["GET", "POST"],
    "ITEM_METHODS": ["GET", "PUT", "DELETE"],
    "ENFORCE_IF_MATCH": False,

    "RETURN_MEDIA_AS_BASE64_STRING": False,
    "RETURN_MEDIA_AS_URL": True,
    "MEDIA_ENDPOINT": "files",
    "MEDIA_PATH": os.path.join(os.environ["PYOR_DATA"], "files"),
    "EXTENDED_MEDIA_INFO": ["filename", "original_filename", "content_type", "length", "md5", "upload_date"],
    "AUTO_COLLAPSE_MULTI_KEYS": True,

    "XML": False,

    "SWAGGER_INFO": {
        "title": "Pyor API",
        "version": "1.0",
        "description": "API to access worker and queue configuratons, register tasks, start them with given "
                       "parameters and monitor the results.",
        "schemes": ["http", "https"],
    },

    "DOMAIN": {}
}