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
try:
    with open(os.getenv('DJANGO_SECRET_KEY_FILE', '')) as f:
        SECRET_KEY = f.read()
except FileNotFoundError:
    SECRET_KEY = ''

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = bool(os.getenv('DREIFALTIGKEIT_DEBUG'))

ALLOWED_HOSTS = [os.getenv('DREIFALTIGKEIT_HOST', '*')]  # List of hosts, e. g. ['*']

SITE_ID = os.getenv('DREIFALTIGKEIT_SITE_ID', 'parish')  # 'parish' or 'kindergarden'
LINK_TO_OTHER_SITE = os.getenv('DREIFALTIGKEIT_LINK_TO_OTHER_SITE', '#')  # URL or at least '#'

WSGI_APPLICATION = 'dreifaltigkeit_wsgi.application'


# Static files (CSS, JavaScript, Images) and media
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static')

MEDIA_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'media')


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

try:
    with open(os.getenv('POSTGRES_PASSWORD_FILE', '')) as f:
        POSTGRES_PASSWORD = f.read()
except FileNotFoundError:
    POSTGRES_PASSWORD = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dreifaltigkeit',
        'USER': 'dreifaltigkeit',
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': os.getenv('PGHOST', ''),
        'PORT': '',
    }
}
