import os

if os.environ["ENV"] == "development":
    DEBUG = True