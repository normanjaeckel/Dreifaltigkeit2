from collections import defaultdict

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
