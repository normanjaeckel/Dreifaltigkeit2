from django.apps import AppConfig
from django.conf import settings
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy


class DreifaltigkeitAppConfig(AppConfig):
    """
    Django application configuration for this website.
    """

    name = "dreifaltigkeit"
    verbose_name = format_lazy(
        "{headline} ({site_id})",
        headline=gettext_lazy("Homepage der Dreifaltigkeitskirchgemeinde"),
        site_id=settings.SITE_ID,
    )
