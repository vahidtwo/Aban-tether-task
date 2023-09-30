from config.base import *  # noqa

INSTALLED_APPS = ["debug_toolbar", *INSTALLED_APPS]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", *MIDDLEWARE]
