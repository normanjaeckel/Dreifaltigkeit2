from itertools import chain

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.formats import localize
from django.utils.timezone import localtime, now
from django.utils.translation import ugettext_lazy
from django_ical.views import ICalFeed

from .models import Announcement, Event


class ParishFeed(Feed):
    """
    RSS Feed for coming events and announcements.
    """
    title = ugettext_lazy('Aktuelles aus der Dreifaltigkeitskirchgemeinde')

    description = ugettext_lazy(
        'Aktuelle Termine, Informationen und Ankündigungen der Ev.-Luth. '
        'Dreifaltigkeitskirchgemeinde Leipzig.')

    feed_copyright = ugettext_lazy(
        'Copyright Ev.-Luth. Dreifaltigkeitskirchgemeinde Leipzig. Alle '
        'Rechte vorbehalten.')

    def link(self):
        return reverse('home')

    def items(self):
        coming_events = Event.objects.get_coming_events()
        announcements = Announcement.objects.filter(end__gte=now()).reverse()
        articles = sorted(chain(coming_events, announcements), key=lambda article: article.time_sort)
        return articles

    def item_title(self, item):
        """
        Customized title for the item: For events we use the title and the date.
        For announcements we use the title.
        """
        if type(item) == Event:
            item_title = ' – '.join((item.title, localize(localtime(item.begin))))
        else:
            # type(item) == Announcement
            item_title = item.title
        return item_title

    def item_description(self, item):
        """
        Customized description for the item: For events we use place and
        content. For announcements we use the short text. People can read the
        long text by following the link.
        """
        if type(item) == Event:
            item_description = item.place
            if item.content:
                if item.place:
                    item_description += ': '
                item_description += item.content
        else:
            # type(item) == Announcement
            item_description = item.short_text
        return item_description

    def item_link(self, item):
        """
        Customized link for the item: For events we use get_absolute_url(). For
        announcements we use the announcement detail page with long_text if it
        exists, else we use link to home view.
        """
        if type(item) == Event:
            item_link = item.get_absolute_url() or self.link()
        else:
            # type(item) == Announcement
            if item.long_text:
                item_link = item.get_absolute_url()
            else:
                item_link = self.link()
        return item_link

    def item_guid(self, item):
        """
        Customized GUID for the item: We use the auto filled uuid field for
        this.
        """
        return item.uuid

    item_guid_is_permalink = False


class EventFeed(ICalFeed):
    """
    ICal feed of all events that are shown in calendar.
    """

    # This is a Formal Public Identifiers according to ISO/IEC 9070:1991,
    # see RFC 5545 p. 78.
    product_id = '-//Ev.-Luth. Dreifaltigkeitskirchgemeinde Leipzig//Kalender//DE'

    title = ugettext_lazy('Termine der Dreifaltigkeitskirchgemeinde')

    description = ugettext_lazy(
        'Besondere Termine und Veranstaltungen der Ev.-Luth. '
        'Dreifaltigkeitskirchgemeinde Leipzig.')

    def link(self):
        return reverse('events')

    def items(self):
        return Event.objects.all()

    def item_title(self, item):
        """
        We just use event title field.
        """
        return item.title

    def item_description(self, item):
        """
        Customized description for the item: We just use event content field.
        """
        return item.content

    def item_link(self, item):
        """
        Customized link for the item: We just use event get_absolute_url()
        method.
        """
        return item.get_absolute_url() or self.link()

    def item_guid(self, item):
        """
        Customized GUID for the item: We use the auto filled uuid field for
        this.
        """
        return item.uuid

    def item_start_datetime(self, item):
        """
        We just use event begin field.
        """
        return item.begin

    def item_end_datetime(self, item):
        """
        We just use event end property.
        """
        return item.end

    def item_location(self, item):
        """
        We just use event place field as location.
        """
        return item.place
