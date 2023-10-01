from config import env

# https://docs.celeryproject.org/en/stable/userguide/configuration.html
# celery Conf
CELERY_BROKER_URL = f"redis://{env('REDIS_HOST')}:6379/2"
result_backend = f"redis://{env('REDIS_HOST')}:6379/1"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_MAX_RETRIES = 3
