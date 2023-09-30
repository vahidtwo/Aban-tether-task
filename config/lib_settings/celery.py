from config import env

# https://docs.celeryproject.org/en/stable/userguide/configuration.html
# celery Conf
CELERY_BROKER_URL = f"redis://{env('REDIS_HOST')}/2"
CELERY_RESULT_BACKEND = f"redis://{env('REDIS_HOST')}"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds
CELERY_TASK_TIME_LIMIT = 30  # seconds
CELERY_TASK_MAX_RETRIES = 3
