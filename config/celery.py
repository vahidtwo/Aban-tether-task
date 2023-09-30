from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.production")

app = Celery("aban_tether")
app.config_from_object("django.conf:lib_settings", namespace="CELERY")
app.conf.timezone = "Asia/Tehran"

app.autodiscover_tasks()


# Load task modules from all registered Django app configs.
packages = []
app.autodiscover_tasks(packages=packages)
