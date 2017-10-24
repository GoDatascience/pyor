from celery import Celery
from pyor.celery import config

app = Celery("pyor")
app.config_from_object(config)

if __name__ == '__main__':
    app.start()