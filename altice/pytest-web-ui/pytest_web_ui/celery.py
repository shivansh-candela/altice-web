from __future__ import absolute_import,unicode_literals
from asyncio import tasks
from datetime import datetime

import os
import sched
from time import time
 
from celery import Celery
from django.conf import settings
from pytz import timezone

# from django_celery_beat.models import PeriodicTask,ClockedSchedule
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pytest_web_ui.settings')

app = Celery('pytest_web_ui')

app.conf.enable_utc=False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
