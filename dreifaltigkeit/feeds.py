from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.formats import localize
from django.utils.timezone import localtime, now
from django.utils.translation import ugettext_lazy

from .models import Announcement, Event


class AnnouncementFeed(Feed):
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
        return Event.objects.get_coming_events() + list(Announcement.objects.filter(end__gte=now()).reverse())

    def item_title(self, item):
        """
        Customized title: For events we use the title and the date. For
        announcements we use the title.
        """
        if type(item) == Event:
            item_title = ' – '.join((item.title, localize(localtime(item.begin))))
        else:
            # type(item) = Announcement
            item_title = item.title
        return item_title

    def item_description(self, item):
        """
        Customized description: For events we use place and content. For
        announcements we use the short text. People can read the long text by
        following the link.
        """
        if type(item) == Event:
            item_description = item.place
            if item.content:
                if item.place:
                    item_description += ': '
                item_description += item.content
        else:
            # type(item) = Announcement
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
            # type(item) = Announcement
            if item.long_text:
                item_link = item.get_absolute_url()
            else:
                item_link = self.link()
        return item_link
