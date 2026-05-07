"""
В этом файле будут Celery-задачи
"""
import os
from celery import Celery, group as celery_group, chord as celery_chord
from celery.schedules import crontab
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

celery_app = Celery('blur_service')
celery_app.conf.broker_url = CELERY_BROKER_URL
celery_app.conf.result_backend = CELERY_RESULT_BACKEND
celery_app.autodiscover_tasks(['tasks'])

celery_app.conf.beat_schedule = {
    'weekly-newsletter': {
        'task': 'tasks.send_weekly_newsletter',
        'schedule': crontab(day_of_week='monday', hour=10, minute=0),
    }
}

group = celery_group
chord = celery_chord
current_app = celery_app
app = celery_app