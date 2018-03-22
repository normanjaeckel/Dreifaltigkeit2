from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView, TemplateView

from .models import Event


THRESHOLD = 30  # Threshold in minutes


class Home(TemplateView):
    """
    Home view.
    """
    template_name = 'home.html'

    def get_context_data(self, **context):
        threshold = timezone.now() - timedelta(minutes=THRESHOLD)
        next_service = Event.objects.filter(type='service', begin__gte=threshold).first()
        return super().get_context_data(
            next_service=next_service,
            **context
        )


class Services(ListView):
    """
    View for all services
    """
    template_name = 'services.html'
    context_object_name = 'services'

    def get_queryset(self):
        threshold = timezone.now() - timedelta(minutes=THRESHOLD)
        return Event.objects.filter(Q(type='service') | Q(type='prayer'), begin__gte=threshold)


class Events(ListView):
    """
    View for all events.
    """
    template_name = 'events.html'
    context_object_name = 'events'
    model = Event


class Imprint(TemplateView):
    """
    Imprint view with legal information.
    """
    template_name = 'imprint.html'
