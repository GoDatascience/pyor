import os

UPLOAD_FOLDER = "/tmp/pyor/uploads"

ALLOWED_SCRIPTS_EXTENSIONS = {"r", "py"}
ALLOWED_EXTENSIONS = {"txt", "csv", "db", "xls", "xlsx", *ALLOWED_SCRIPTS_EXTENSIONS}

if os.environ["ENV"] == "development":
    DEBUG = True