import os

UPLOAD_FOLDER = "/tmp/mreq/uploads"

ALLOWED_EXTENSIONS = {"txt", "csv", "r", "py", "db", "xls", "xlsx"}

if os.environ["ENV"] == "dev":
    DEBUG = True