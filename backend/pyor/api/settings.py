import os

SETTINGS = {
    "DEBUG": True if os.environ.get("ENV") == "development" else False,
    "MONGO_HOST": os.environ["MONGO_HOST"],
    "MONGO_PORT": int(os.environ["MONGO_PORT"]),
    "MONGO_DBNAME": os.environ["MONGO_DBNAME"],

    "URL_PREFIX": "api",
    "API_VERSION": "v1",

    "PAGINATION_DEFAULT": 10,

    "DATE_FORMAT": "%Y-%m-%dT%H:%M:%S.%f%z",

    "RESOURCE_METHODS": ["GET", "POST"],
    "ITEM_METHODS": ["GET", "PUT", "DELETE"],

    "RETURN_MEDIA_AS_BASE64_STRING": False,
    "RETURN_MEDIA_AS_URL": True,
    "MEDIA_ENDPOINT": "files",
    "MEDIA_PATH": os.path.join(os.environ["PYOR_DATA"], "files"),
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