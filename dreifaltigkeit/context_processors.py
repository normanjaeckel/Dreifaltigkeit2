from collections import defaultdict

from django.conf import settings

from .models import FlatPage


def flat_pages(request):
    """
    Context processor to add all root and non-root flat pages to the context of
    all views. Used for the main menu. Flat pages that are not in the menu are
    excluded.
    """
    context = defaultdict(list)
    for flat_page in FlatPage.objects.all():
        if flat_page.is_in_menu():
            key = 'pages_' + flat_page.category.replace('-', '')
            context[key].append(flat_page)
    return context


def site_id(request):
    """
    Adds SITE_ID and LINK_TO_OTHER_SITE to the context of all views. Used to
    differentiate between site for parish and kindergarden.
    """
    return {
        'SITE_ID': settings.SITE_ID,
        'LINK_TO_OTHER_SITE': settings.LINK_TO_OTHER_SITE,
    }


def truncate_length(request):
    """
    Adds number of chars to the context used to truncate event content.
    """
    return {
        'TRUNCATE_LENGTH': settings.TRUNCATE_LENGTH,
    }


def default_images(request):
    """
    Adds all default images to the context. We use built in random filter to
    get random default images.
    """
    return {
        'DEFAULT_IMAGES': settings.DEFAULT_IMAGES,
    }
