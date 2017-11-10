import os

from pyor.models import LAST_UPDATED, DATE_CREATED, ETAG, VERSION, LATEST_VERSION, VERSIONS, VERSION_ID_SUFFIX, ID_FIELD

SETTINGS = {
    "DEBUG": True if os.environ.get("ENV") == "development" else False,
    "SECRET_KEY": os.environ.get("SECRET_KEY", "dev"),
    "SALT": os.environ.get("SALT", "dev"),
    # MongoDb
    "MONGO_HOST": os.environ["MONGO_HOST"],
    "MONGO_PORT": int(os.environ["MONGO_PORT"]),
    "MONGO_DBNAME": os.environ["MONGO_DBNAME"],
    # Redis
    "REDIS_HOST": os.environ["REDIS_HOST"],
    "REDIS_PORT": int(os.environ["REDIS_PORT"]),
    # Mail
    "MAIL_SERVER": os.environ["MAIL_SERVER"],
    "MAIL_PORT": int(os.environ["MAIL_PORT"]),
    "MAIL_USE_SSL": os.environ["MAIL_USE_SSL"] == "True",
    "MAIL_USE_TLS": os.environ["MAIL_USE_TLS"] == "True",
    "MAIL_USERNAME": os.environ.get("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD"),
    "MAIL_DEFAULT_SENDER": os.environ.get("MAIL_DEFAULT_SENDER"),
    # Api
    "URL_PREFIX": "api",
    ## Configs
    "DOMAIN": {},
    "PAGINATION_DEFAULT": 10,
    "DATE_FORMAT": "%Y-%m-%dT%H:%M:%S.%fZ",
    "XML": False,
    "RESOURCE_METHODS": ["GET", "POST"],
    "ITEM_METHODS": ["GET", "PUT", "DELETE"],
    "ENFORCE_IF_MATCH": False,
    ## Fields
    "ID_FIELD": ID_FIELD,
    "LAST_UPDATED": LAST_UPDATED,
    "DATE_CREATED": DATE_CREATED,
    "ETAG": ETAG,
    "VERSION": VERSION,
    "LATEST_VERSION": LATEST_VERSION,
    "VERSIONS": VERSIONS,
    "VERSION_ID_SUFFIX": VERSION_ID_SUFFIX,
    ## Media
    "RETURN_MEDIA_AS_BASE64_STRING": False,
    "RETURN_MEDIA_AS_URL": True,
    "MEDIA_ENDPOINT": "files",
    "MEDIA_PATH": os.path.join(os.environ["PYOR_DATA"], "files"),
    "EXTENDED_MEDIA_INFO": ["filename", "original_filename", "content_type", "length", "md5", "upload_date"],
    "AUTO_COLLAPSE_MULTI_KEYS": True,
    ## Auth
    "OAUTH2_CACHE_TYPE": "redis",
    "SECURITY_POST_LOGIN_VIEW": "http://"+os.environ["FRONTEND_URL"],
    "SECURITY_POST_LOGOUT_VIEW": "http://"+os.environ["FRONTEND_URL"],
    "SECURITY_CONFIRMABLE": True,
    "SECURITY_REGISTERABLE": False,
    "SECURITY_PASSWORD_SALT": "salt", # TODO
    ## Swagger
    "SWAGGER_INFO": {
        "title": "Pyor API",
        "version": "1.0",
        "description": "API to access worker and queue configuratons, register tasks, start them with given "
                       "parameters and monitor the results.",
        "schemes": ["http", "https"],
    },

}