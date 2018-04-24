
from __future__ import absolute_import
import os
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'useMongo.settings')
from celery.contrib import rdb

from django.conf import settings
from celery import Celery

app = Celery()

# This reads, e.g., CELERY_ACCEPT_CONTENT = ['json'] from settings.py:
app.config_from_object('django.conf:settings')

# For autodiscover_tasks to work, you must define your tasks in a file called 'tasks.py'.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))

app.conf.beat_schedule = {
     'add-every-monday-morning': {
        'task': 'fanpages.tasks.crontab_get_posts',
        'schedule': crontab(hour=17, minute=0),
    },
}

app.conf.timezone = 'UTC'
