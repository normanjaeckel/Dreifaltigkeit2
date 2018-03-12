import collections
import datetime
import json

from django.db import models
from django.utils.formats import localize
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy

EVENT_TYPES = (
    ('service', ugettext_lazy('Gottesdienst')),
    ('prayer', ugettext_lazy('Andacht')),
    ('concert', ugettext_lazy('Konzert')),
    ('gathering', ugettext_lazy('Treff')),
    ('period-of-reflection', ugettext_lazy('Rüstzeit')),
    ('default', ugettext_lazy('Sonstige Veranstaltung')),
    ('hidden', ugettext_lazy('Nichtöffentliche Veranstaltung')),
)

class EventTypes:
    """
    Container object for all event types.
    """
    def __init__(self):
        self.event_types = collections.OrderedDict(**{
            'service': {
                'verbose_name': ugettext_lazy('Gottesdienst'),
                'color': 'blue',
            },
            'prayer': {
                'verbose_name': ugettext_lazy('Andacht'),
                'color': 'red',
            },
            'concert': {
                'verbose_name': ugettext_lazy('Konzert'),
                'color': 'yellow',
            },
            'default': {
                'verbose_name': ugettext_lazy('Sonstige Veranstaltung'),
                'color': 'green',
            },
            'hidden': {
                'verbose_name': ugettext_lazy('Nichtöffentliche Veranstaltung'),
                'color': 'grey',
            },
        })

    def get_choices(self):
        for name, event_type in self.event_types.items():
            yield name, event_type['verbose_name']


class Event(models.Model):
    """
    Model for events.

    Most important field is the type of the event.
    """
    type = models.CharField(
        ugettext_lazy('Veranstaltungstyp'),
        max_length=255,
        choices=EventTypes().get_choices(),
        default='default',
        help_text=ugettext_lazy('Gottesdienste und Konzerte werden auf den besonderen Seite zusätzlich angezeigt.'),
    )

    title = models.CharField(
        ugettext_lazy('Titel'),
        max_length=255,
        help_text=ugettext_lazy('Kurzer Titel der Veranstaltung'),
    )

    content = models.TextField(
        ugettext_lazy('Inhalt'),
        blank=True,
        help_text=ugettext_lazy('Beschreibung der Veranstaltung.'),
    )

    begin = models.DateTimeField(
        ugettext_lazy('Beginn'),
    )

    duration = models.PositiveIntegerField(
        ugettext_lazy('Dauer in Minuten'),
        null=True,
        blank=True,
        help_text=ugettext_lazy(
            'Wenn nichts angegeben ist, wird keine Zeit für das Ende der '
            'Veranstaltung angezeigt.'),
    )

    on_home_before_begin = models.PositiveIntegerField(
        ugettext_lazy('Auf der Startseite (in Tagen)'),
        default=0,
        help_text=ugettext_lazy(
            'Die Veranstaltung erscheint so viele Tage vor Beginn auf der '
            'Startseite. Wählen Sie 0, wenn die Veranstaltung niemals auf der '
            'Startseite erscheinen soll. Der nächste Gottesdienste und das '
            'nächste Konzert erscheinen immer auf der Startseite, egal, was '
            'hier eingestellt ist.'),
    )

    class Meta:
        ordering = ('begin',)
        verbose_name = ugettext_lazy('Veranstaltung')
        verbose_name_plural = ugettext_lazy('Veranstaltungen')
        permissions = (
            (
                'can_see_hidden_events',
                ugettext_lazy('Darf nichtöffentliche Veranstaltungen sehen'),
            ),
        )

    def __str__(self):
        return ' – '.join((localize(localtime(self.begin)), self.title))

    @property
    def end(self):
        duration = self.duration or 0
        return self.begin + datetime.timedelta(minutes=duration)

    @property
    def fc_data(self):
        """
        Returns a string containing all data for the fullcalendar event object
        as JSON.
        """
        return json.dumps({
            'title': self.get_type_display() + ': ' + self.title,
            'start': self.begin.isoformat(),
            'end': self.end.isoformat(),
            'color': EventTypes().event_types[self.type]['color']
        })


class MediaFile(models.Model):
    """
    Model for uploaded files like images.
    """
    mediafile = models.FileField(
        ugettext_lazy('Datei'),
        max_length=255,
        help_text=ugettext_lazy(
            'Achtung: Hochgeladene Dateien sind für jeden im Internet '
            'sichtbar.'),
    )

    uploaded_on = models.DateTimeField(
        ugettext_lazy('Hochgeladen am'),
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-uploaded_on',)
        verbose_name = ugettext_lazy('Datei')
        verbose_name_plural = ugettext_lazy('Dateien')

    def __str__(self):
        return self.mediafile.url
