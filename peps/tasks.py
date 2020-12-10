from .celery import app
from datetime import timedelta


@app.task()
def remind_recipients():
    print('remind_recipients')
