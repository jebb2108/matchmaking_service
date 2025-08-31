from celery import Celery

app = Celery(
    'app.core.celeryconfig',
    broker='redis://localhost',
    backend='redis://localhost',
    broker_connection_retry_on_startup=True,
    include=['app.tasks.matchmaking',]
)

# Настройки
app.conf.update(
    expire_result=3600,
    task_serializer='json',
    result_serializer='json',
    task_ignore_result=False,
    task_track_started=True,
)


