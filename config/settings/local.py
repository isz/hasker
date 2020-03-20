import os

from .base import *
from .secret import *

DEBUG = True

INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

INTERNAL_IPS = ['127.0.0.1',]


ANSWERS_PER_PAGE = 2
QUESTIONS_PER_PAGE = 5
QUESTIONS_PER_SEARCH_PAGE = 10
TRENDS_PER_PAGE = 5

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True