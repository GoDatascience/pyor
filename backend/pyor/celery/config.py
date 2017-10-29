broker_url = 'amqp://pyor:pyor@rabbitmq:5672/pyor'
result_backend = 'pyor.celery.backend.PyorBackend'

task_track_started = True
result_expires = None
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True

imports = ('pyor.celery.tasks',)