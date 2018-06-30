"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

from dreifaltigkeit.general_settings import *  # noqa

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 'parish'
# SITE_ID = 'kindergarden'
LINK_TO_OTHER_SITE = '#'

WSGI_APPLICATION = 'dreifaltigkeit_wsgi.application'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'deployment', 'static')


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DEVELOPMENT_DATABASE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'db_dreifaltigkeit_{}.sqlite3'.format(SITE_ID)
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DEVELOPMENT_DATABASE_PATH,
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'dreifaltigkeit_{}'.format(SITE_ID),
#         'USER': 'dreifaltigkeit',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }
