broker_url = 'amqp://pyor:pyor@rabbitmq:5672/pyor'
result_backend = 'redis://redis:6379'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
enable_utc = True

imports = ('pyor.tasks',)