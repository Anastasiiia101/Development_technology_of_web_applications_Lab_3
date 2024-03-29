from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = Celery('shortener')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

from kombu import Exchange, Queue

app.conf.task_queues = (
    Queue('email', Exchange('direct'), routing_key='email'),
    Queue('url_dump', Exchange('direct'), routing_key='url_dump'),
)
