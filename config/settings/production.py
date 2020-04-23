import os
from .base import *
from .secret import *

DEBUG = True

MEDIA_ROOT = os.environ['MEDIA_ROOT']
STATIC_ROOT = os.environ.get('STATIC_ROOT', '')

print(MEDIA_ROOT)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ANSWERS_PER_PAGE = 30
QUESTIONS_PER_PAGE = 20
QUESTIONS_PER_SEARCH_PAGE = 20
TRENDS_PER_PAGE = 20

EMAIL_USE_TLS = True