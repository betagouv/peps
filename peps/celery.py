import os
import dotenv
from celery import Celery
from celery.schedules import crontab

dotenv.load_dotenv()

app = Celery('peps',
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL'),
    include=['peps.tasks']
)

app.conf.beat_schedule = {
    "remind-recipients": {
        "task": "peps.tasks.remind_recipients",
        "schedule": crontab(minute='*/1')
    }
}
app.conf.timezone = 'UTC'

if __name__ == '__main__':
    app.start()
