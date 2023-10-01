from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.production")

app = Celery("aban_tether")
app.config_from_object("config.lib_settings.celery", namespace="CELERY")
app.conf.timezone = "Asia/Tehran"

app.autodiscover_tasks()


# Load task modules from all registered Django app configs.
packages = ["apps.exchange"]
app.autodiscover_tasks(packages=packages)


def check_task_is_running(task_import_path: str) -> bool:  # TODO str is not suitable type annotate
    """check one task is running in celery or not"""
    is_compute_task_is_running = False
    for worker_name, tasks in app.control.inspect().active().items():
        for task in tasks:
            if task["name"] == task_import_path:
                is_compute_task_is_running = True
                break
    return is_compute_task_is_running
