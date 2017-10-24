from celery import Celery

app = Celery("pyor")
app.config_from_object("pyor.celeryconfig")

if __name__ == '__main__':
    app.start()