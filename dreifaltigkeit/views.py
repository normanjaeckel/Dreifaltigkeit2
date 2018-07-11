from datetime import timedelta

from django.conf import settings
from django.db.models import Q
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView

from .models import Announcement, Event, FlatPage as FlatPageModel


class Home(TemplateView):
    """
    Home view.
    """
    def get_template_names(self):
        """
        Returns the template name: home_parish.html or home_kindergarden.html.
        """
        return ['home_{}.html'.format(settings.SITE_ID)]

    def get_context_data(self, **context):
        threshold = timezone.now() - timedelta(minutes=settings.THRESHOLD)
        next_service = Event.objects.filter(type='service', begin__gte=threshold).last()
        announcements = Announcement.objects.filter(end__gte=timezone.now()).reverse()
        coming_events_queryset = (Event.objects
            .exclude(type='service')
            .exclude(on_home_before_begin=0)
            .filter(begin__gte=threshold)
            .reverse()
        )
        coming_events = []
        for coming_event in coming_events_queryset:
            time_to_show = timezone.now() + timedelta(
                days=coming_event.on_home_before_begin)
            if coming_event.begin <= time_to_show:
                coming_events.append(coming_event)

        return super().get_context_data(
            next_service=next_service,
            coming_events=coming_events,
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
        threshold = timezone.now() - timedelta(minutes=settings.THRESHOLD)
        return Event.objects.filter(Q(type='service') | Q(type='prayer'), begin__gte=threshold).reverse()


class Events(ListView):
    """
    View for all events.
    """
    template_name = 'events.html'
    context_object_name = 'events'
    model = Event


class SingleEvent(DetailView):
    """
    View for a single event.
    """
    template_name = 'single_event.html'
    model = Event

    def get_object(self):
        """
        Customized method: Send HTTP 404 if event type is service or prayer or
        there is no event content.
        """
        event = super().get_object()
        if event.type in ('service', 'prayer') or not event.content:
            message = 'Event {} is a service or prayer or has no content.'.format(event.title)
            raise Http404(message)
        return event


class FlatPage(TemplateView):
    """
    View for all root and non-root flat pages.
    """
    root = False
    template_name = 'flat_page.html'

    def get_context_data(self, *args, **kwargs):
        """
        Customized method: Adds flat page instance to the context and sends
        HTTP 404 if page does not exist.
        """
        context = super().get_context_data(*args, **kwargs)
        if self.root:
            category='{}_root'.format(settings.SITE_ID)
        else:
            category=context['category']
        context['flat_page'] = get_object_or_404(
            FlatPageModel, category=category, url=context['page'])
        return context

    def get(self, request, *args, **kwargs):
        """
        Overridden method. Returns HTTP 301 if flat page is only for redirect.
        """
        context = self.get_context_data(**kwargs)
        if context['flat_page'].redirect:
            return HttpResponsePermanentRedirect(context['flat_page'].redirect)
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
