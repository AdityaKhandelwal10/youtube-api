#Defines the celery instance for the app

from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','youtube_api.settings')

app = Celery('youtube_api')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-youtube-data-every-10-secs':{
        'task':'video.tasks.fetchVideo',
        'schedule':30.0
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


