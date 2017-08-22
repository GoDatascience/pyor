import os

if os.environ["ENV"] == "dev":
    DEBUG = True