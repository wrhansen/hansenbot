'''
NOTE: This file is deprecated, trying a solution without needing celery
'''
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

from django.conf import settings

app = Celery("website")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
