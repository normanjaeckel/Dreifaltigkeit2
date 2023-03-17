"""
Small helper script to create settings files and WSGI file from templates.
"""
import os
from string import Template
from textwrap import dedent

from django.utils.crypto import get_random_string

SITE_IDS = {
    'parish': 'kindergarden',
    'kindergarden': 'parish',
}

# DATABASES_DEVELOPMENT = dedent(
#     """
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(
#                 os.path.dirname(os.path.abspath(__file__)),
#                 'db_dreifaltigkeit_{}.sqlite3'.format(SITE_ID)
#             ),
#         }
#     }
#     """
# ).strip()

DATABASES_PRODUCTION = dedent(
    """
    DB_HOST = os.getenv('PG_HOST', '')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'dreifaltigkeit_{}'.format(SITE_ID),
            'USER': 'dreifaltigkeit',
            'PASSWORD': '',
            'HOST': DB_HOST,
            'PORT': '',
        }
    }
    """
).strip()


def create_settings():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    for site_id in ('parish', 'kindergarden'):
        new_settings_file_path = os.path.join(base_dir, 'dreifaltigkeit_{}_settings.py'.format(site_id))
        if not os.path.exists(new_settings_file_path):
            default_settings_file_path = os.path.join(base_dir, 'dreifaltigkeit_settings.py.tpl')
            with open(default_settings_file_path) as default_settings_file:
                secret_key = get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                host = os.environ.get('DREIFALTIGKEIT_{}_HOST'.format(site_id.upper()))
                other_site = os.environ.get('DREIFALTIGKEIT_{}_HOST'.format(SITE_IDS[site_id].upper()))
                databases = DATABASES_PRODUCTION  # if host else DATABASES_DEVELOPMENT
                context = dict(
                    secret_key=secret_key,
                    debug=not host,
                    host=host if host else '*',
                    site_id=site_id,
                    link_to_other_site='https://{}'.format(other_site) if other_site else '#',
                    databases=databases,
                )
                settings = Template(default_settings_file.read()).substitute(**context)
                with open(new_settings_file_path, 'w') as new_settings_file:
                    new_settings_file.write(settings)
            print('Settings file {} successfully created.'.format(new_settings_file_path))


def create_wsgi():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    new_wsgi_file_path = os.path.join(base_dir, 'dreifaltigkeit_wsgi.py')
    if not os.path.exists(new_wsgi_file_path):
        default_wsgi_file_path = os.path.join(base_dir, 'dreifaltigkeit_wsgi.py.tpl')
        with open(default_wsgi_file_path) as default_wsgi_file:
            with open(new_wsgi_file_path, 'w') as new_wsgi_file:
                new_wsgi_file.write(default_wsgi_file.read())
        print('WSGI file {} successfully created.'.format(new_wsgi_file_path))


if __name__ == '__main__':
    create_settings()
    create_wsgi()
