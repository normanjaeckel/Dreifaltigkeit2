from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class DreifaltigkeitAppConfig(AppConfig):
    """
    Django application configuration for this website.
    """
    name = 'dreifaltigkeit'
    verbose_name = ugettext_lazy('Homepage der Dreifaltigkeitskirchgemeinde')
