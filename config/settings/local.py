import os

from .base import *

SECRET_KEY = "ihgvbishgovhwergoewrhjio"

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

MEDIA_ROOT = root("stackoverflow/media")

db = DATABASES['default']
db["HOST"] = "127.0.0.1"
db["NAME"] = "postgres"
db["USER"] = "postgres"
db["PASSWORD"] = "postgres"


INTERNAL_IPS = [
    "127.0.0.1",
]

ANSWERS_PER_PAGE = 2
QUESTIONS_PER_PAGE = 5
QUESTIONS_PER_SEARCH_PAGE = 10
TRENDS_PER_PAGE = 5

EMAIL_USE_TLS = True

try:
    from .secret import EMAIL_FROM, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
except:
    pass
