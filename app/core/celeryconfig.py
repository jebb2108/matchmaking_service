from celery import Celery

app = Celery(
    'celery',
    broker='redis://localhost',
    backend='redis://localhost',
    include=['tasks.matchmaking', 'tasks.notification']
)

# Настройки
app.conf.update(
    expire_result=3600,
    task_serializer='json',
    result_serializer='json',
    task_ignore_result=False,
    task_track_started=True,
)

if __name__ == '__main__':
    app.start()

