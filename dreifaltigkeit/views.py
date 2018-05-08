from datetime import timedelta

from django.db.models import Q
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView

from .models import Announcement, Event, FlatPage


THRESHOLD = 30  # Threshold in minutes


class Home(TemplateView):
    """
    Home view.
    """
    template_name = 'home.html'

    def get_context_data(self, **context):
        threshold = timezone.now() - timedelta(minutes=THRESHOLD)
        next_service = Event.objects.filter(type='service', begin__gte=threshold).first()
        announcements = Announcement.objects.filter(end__gte=timezone.now()).reverse()
        return super().get_context_data(
            next_service=next_service,
            announcements=announcements,
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


class Flatpage(TemplateView):
    """
    View for all flatpages (parish, music, youth).
    """
    template_name = 'flatpage.html'

    def get_context_data(self, *args, **kwargs):
        """
        Customized method: Adds flatpage instance to the context and sends
        HTTP 404 if page does not exist.
        """
        context = super().get_context_data(*args, **kwargs)
        context['flatpage'] = get_object_or_404(
            FlatPage, category=context['category'], url=context['page'])
        return context

    def get(self, request, *args, **kwargs):
        """
        Overridden method. Returns HTTP 301 if flatpage is only for redirect.
        """
        context = self.get_context_data(**kwargs)
        if context['flatpage'].redirect:
            return HttpResponsePermanentRedirect(context['flatpage'].redirect)
        return self.render_to_response(context)


class Imprint(TemplateView):
    """
    Imprint view with legal information.
    """
    template_name = 'imprint.html'


class Announcements(DetailView):
    """
    View for details of an announcement.
    """
    template_name = 'announcements.html'
    model = Announcement

    def get_object(self):
        """
        Customized method: Send HTTP 404 if time is elapsed or if there is
        no long_text.
        """
        announcement = super().get_object()
        if announcement.end < timezone.now() or not announcement.long_text:
            message = 'Announcement {} is elapsed or has no long_text.'.format(
                announcement.title)
            raise Http404(message)
        return announcement
