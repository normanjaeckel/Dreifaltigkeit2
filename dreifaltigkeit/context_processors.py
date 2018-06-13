from collections import defaultdict

from django.conf import settings

from .models import FlatPage


def flatpages(request):
    """
    Context processor to add all flatpages to the context of all views.
    Used for the main menu.
    """
    context = defaultdict(list)
    for flatpage in FlatPage.objects.all():
        key = 'pages_' + flatpage.category.replace('-', '')
        context[key].append(flatpage)
    return context


def site_id(request):
    """
    Adds SITE_ID to the context of all views. Used to differentiate between
    site for parish and kindergarden.
    """
    return {'SITE_ID': settings.SITE_ID}
