"""
WSGI config.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os, site

# site.addsitedir('/path/to/Dreifaltigkeit')
# site.addsitedir('/path/to/Dreifaltigkeit/.virtualenv/lib/python3.6/site-packages')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dreifaltigkeit_settings')
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    raise RuntimeError(
        'You have to set DJANGO_SETTINGS_MODULE environment variable.')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
