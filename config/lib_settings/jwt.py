import datetime

from config import env


# TODO refactor it
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(seconds=env("ACCESS_TOKEN_LIFETIME", default=60 * 60 * 24 * 7)),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(seconds=env("REFRESH_TOKEN_LIFETIME", default=60 * 60 * 24 * 1)),
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
