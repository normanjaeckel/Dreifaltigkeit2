import collections
import datetime
import json
import locale
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template import Context, Template
from django.urls import reverse
from django.utils.formats import localize
from django.utils.timezone import localtime, now
from django.utils.translation import get_language, ugettext_lazy


class FlatPage(models.Model):
    """
    Model for flat pages.

    Every flat page belongs to one of five categories: The pages for parish_root
    and kindergarden_root live at the root level of the menu. The pages for the
    other three categories parish, music and youth live at a sublevel.

    Flat pages containing a slash in their URL live at a lower level and to not
    appear in main menu.

    The fields category, url, title, ordering and redirect are readonly in
    admin. The model instances are created via migration file.
    """

    category = models.CharField(
        ugettext_lazy("Kategorie"),
        max_length=255,
        choices=(
            ("gemeinde", ugettext_lazy("Gemeinde")),
            ("kirchenmusik", ugettext_lazy("Kirchenmusik")),
            ("kinder-und-jugend", ugettext_lazy("Kinder und Jugend")),
            ("parish_root", ugettext_lazy("Gemeinde Hauptmenü")),
            ("kindergarden_root", ugettext_lazy("Kindergarten Hauptmenü")),
        ),
    )

    url = models.CharField(ugettext_lazy("URL"), max_length=255)

    title = models.CharField(ugettext_lazy("Titel"), max_length=255)

    menu_title = models.CharField(
        ugettext_lazy("Eintrag im Menü"),
        blank=True,
        max_length=255,
        help_text=ugettext_lazy(
            "Wenn hier nichts eingetragen ist, wird der Titel zugleich als "
            "Bezeichnung im Menü verwendet."
        ),
    )

    ordering = models.IntegerField(ugettext_lazy("Sortierung"))

    redirect = models.CharField(
        ugettext_lazy("Weiterleitung"),
        blank=True,
        max_length=255,
        help_text=ugettext_lazy(
            "Wenn eine Weiterleitung eingerichtet ist, wird kein zusätzlicher "
            "Inhalt angezeigt."
        ),
    )

    content = models.TextField(
        ugettext_lazy("Inhalt"),
        blank=True,
        default="<p>\n\n\n\n</p>",
        help_text=ugettext_lazy("Inhalt der Seite in HTML."),
    )

    class Meta:
        ordering = ("ordering",)
        verbose_name = ugettext_lazy("Statische Seite")
        verbose_name_plural = ugettext_lazy("Statische Seiten")

    def __str__(self):
        result = self.get_category_display()
        if not self.is_in_menu():
            result += " – _____"
        return " – ".join((result, self.title))

    def get_absolute_url(self):
        if self.category in ("parish_root", "kindergarden_root"):
            url = reverse("flat_page_root", kwargs={"page": self.url})
        else:
            url = reverse(
                "flat_page", kwargs={"category": self.category, "page": self.url}
            )
        return url

    def get_menu_title(self):
        """
        Returns the title used in the main menu. This is the menu_title. If
        this field is empty, the title is returned.
        """
        return self.menu_title or self.title

    def is_in_menu(self):
        """
        Returns True if URL does not contain a slash so it is not a subpage.
        """
        return self.url.find("/") == -1


def validate_year_month_number(value):
    """
    Validator for month field of MonthlyText model.
    """
    if not 99999 < value < 1000000:
        raise ValidationError(ugettext_lazy("Die Zahl muss sechsstellig sein."))
    if not 2017 < int(str(value)[:4]) < 2200:
        raise ValidationError(
            ugettext_lazy(
                "Die ersten vier Ziffern (Jahreszahl) müssen zwischen 2018 und "
                "2199 liegen."
            )
        )
    if not 0 < int(str(value)[-2:]) < 13:
        raise ValidationError(
            ugettext_lazy(
                "Die letzten beiden Ziffern (Monatszahl) müssen zwischen 01 und "
                "12 liegen."
            )
        )


class YearlyText(models.Model):
    """
    Model for yearly texts by the "Ökumenische Arbeitsgemeinschaft für
    Bibellesen – ÖAB" in Berlin.
    """

    year = models.IntegerField(
        ugettext_lazy("Jahr"),
        validators=[MinValueValidator(2018), MaxValueValidator(2199)],
        unique=True,
        help_text=ugettext_lazy("Eingabe als vierstellige Zahl."),
    )

    text = models.TextField(
        ugettext_lazy("Jahreslosung"),
        help_text=ugettext_lazy(
            'Die Jahreslosung der <a href="https://www.oeab.de/">'
            "Ökumenischen Arbeitsgemeinschaft für Bibellesen</a> "
            "erscheint nur auf der Gottesdienstseite. Kein HTML erlaubt."
        ),
    )

    verse = models.CharField(
        ugettext_lazy("Bibelstelle"),
        max_length=255,
        help_text=ugettext_lazy("Beispiel: Joh 19,30."),
    )

    class Meta:
        ordering = ("-year",)
        verbose_name = ugettext_lazy("Jahreslosung")
        verbose_name_plural = ugettext_lazy("Jahreslosungen")

    def __str__(self):
        return str(self.year)


class MonthlyText(models.Model):
    """
    Model for monthly texts by the "Ökumenische Arbeitsgemeinschaft für
    Bibellesen – ÖAB" in Berlin.
    """

    month = models.IntegerField(
        ugettext_lazy("Monat"),
        validators=[validate_year_month_number],
        unique=True,
        help_text=ugettext_lazy(
            "Eingabe als sechsstellige Zahl bestehend aus Jahr und Monat "
            "z. B. 201307 für Juli 2013."
        ),
    )

    text = models.TextField(
        ugettext_lazy("Monatsspruch"),
        help_text=ugettext_lazy(
            'Der Monatsspruch der <a href="https://www.oeab.de/">Ökumenischen '
            "Arbeitsgemeinschaft für Bibellesen</a> erscheint nur auf der "
            "Gottesdienstseite. Kein HTML erlaubt."
        ),
    )

    verse = models.CharField(
        ugettext_lazy("Bibelstelle"),
        max_length=255,
        help_text=ugettext_lazy("Beispiel: Joh 19,30."),
    )

    class Meta:
        ordering = ("-month",)
        verbose_name = ugettext_lazy("Monatsspruch")
        verbose_name_plural = ugettext_lazy("Monatssprüche")

    def __str__(self):
        if get_language() == "de":
            loc = "de_DE"
        elif get_language() == "en":
            loc = "en_US"
        else:
            loc = None
        if loc:
            locale.setlocale(locale.LC_TIME, (loc, "UTF-8"))
        return self.datetime.strftime("%B %Y")

    @property
    def datetime(self):
        """
        Returns a datetime object of the month of this instance.
        """
        return datetime.datetime.strptime(str(self.month), "%Y%m")


class EventTypes:
    """
    Container object for all event types.
    """

    def __init__(self):
        self.event_types = collections.OrderedDict()
        self.event_types["service"] = {
            "verbose_name": ugettext_lazy("Gottesdienst"),
            "color": "darkorange",
        }
        self.event_types["prayer"] = {
            "verbose_name": ugettext_lazy("Andacht"),
            "color": "red",
        }
        self.event_types["concert"] = {
            "verbose_name": ugettext_lazy("Konzert"),
            "color": "green",
        }
        self.event_types["gathering"] = {
            "verbose_name": ugettext_lazy("Treff"),
            "color": "darkcyan",
        }
        self.event_types["period-of-reflection"] = {
            "verbose_name": ugettext_lazy("Rüstzeit"),
            "color": "forestgreen",
        }
        self.event_types["default"] = {
            "verbose_name": ugettext_lazy("Sonstige Veranstaltung"),
            "color": "grey",
        }
        self.event_types["hidden"] = {
            "verbose_name": ugettext_lazy("Nichtöffentliche Veranstaltung"),
            "color": "grey",
        }

    def get_choices(self):
        for name, event_type in self.event_types.items():
            yield name, event_type["verbose_name"]


class EventManager(models.Manager):
    """
    Customized model manager to provide extra manager methods.
    """

    def get_coming_events(self):
        """
        Returns a special filtered and sorted list with coming events for home
        view and RSS feed.
        """
        threshold = now() - datetime.timedelta(minutes=settings.THRESHOLD)
        coming_events_queryset = (
            self.exclude(type="service")
            .exclude(on_home_before_begin=0)
            .filter(begin__gte=threshold)
            .reverse()
        )
        coming_events = []
        for coming_event in coming_events_queryset:
            time_to_show = now() + datetime.timedelta(
                days=coming_event.on_home_before_begin
            )
            if coming_event.begin <= time_to_show:
                coming_events.append(coming_event)
        return coming_events


class Event(models.Model):
    """
    Model for events.

    Most important field is the type of the event.
    """

    objects = EventManager()

    type = models.CharField(
        ugettext_lazy("Veranstaltungstyp"),
        max_length=255,
        choices=EventTypes().get_choices(),
        default="default",
        help_text=ugettext_lazy(
            "Gottesdienste und Andachten werden auf der besonderen Seite "
            "zusätzlich angezeigt. Außerdem beeinflusst der Typ die Farbe im "
            "Kalender."
        ),
    )

    title = models.CharField(
        ugettext_lazy("Titel"),
        max_length=255,
        help_text=ugettext_lazy("Kurzer Titel der Veranstaltung."),
    )

    place = models.CharField(
        ugettext_lazy("Ort"),
        blank=True,
        default="Trinitatiskirche",
        max_length=255,
        help_text=ugettext_lazy(
            "Ort der Veranstaltung, z. B. Trinitatiskirche, Markuskapelle, "
            "Anbau der Trinitatiskirche, Gemeindehaus Dresdner Straße 59."
        ),
    )

    content = models.TextField(
        ugettext_lazy("Inhalt"),
        blank=True,
        help_text=ugettext_lazy("Beschreibung der Veranstaltung. Kein HTML erlaubt."),
    )

    flat_page = models.ForeignKey(
        verbose_name=ugettext_lazy("Statische Seite"),
        to="FlatPage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text=ugettext_lazy(
            "Zusätzliche Verlinkung auf eine statische Seite. Wenn angegeben, "
            "hat der Termin an sich keine eigene Seite mehr und der Inhalt "
            "kann ggf. nicht erreicht werden. Nicht möglich für Gottesdienste "
            "und Andachten."
        ),
    )

    begin = models.DateTimeField(ugettext_lazy("Beginn"))

    duration = models.PositiveIntegerField(
        ugettext_lazy("Dauer (Angabe in Minuten)"),
        null=True,
        blank=True,
        help_text=ugettext_lazy(
            "Wenn nichts angegeben ist, wird keine Zeit für das Ende der "
            "Veranstaltung angezeigt."
        ),
    )

    on_home_before_begin = models.PositiveIntegerField(
        ugettext_lazy("Auf der Startseite (Angabe in Tagen)"),
        default=0,
        help_text=ugettext_lazy(
            "Die Veranstaltung erscheint so viele Tage vor Beginn auf der "
            "Startseite. Wählen Sie 0, wenn die Veranstaltung niemals auf der "
            "Startseite erscheinen soll. Der nächste Gottesdienste und das "
            "nächste Konzert erscheinen immer auf der Startseite, egal, was "
            "hier eingestellt ist."
        ),
    )

    mediafile = models.ForeignKey(
        verbose_name=ugettext_lazy("Bild"),
        to="MediaFile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    for_kids = models.BooleanField(
        ugettext_lazy("Gottesdienst mit Kindergottesdienst"),
        blank=True,
        help_text=ugettext_lazy(
            "Nur bei Gottesdiensten kann hier eingestellt werden, ob das "
            "Kindergottesdienst-Logo angezeigt werden soll. Sonst hat dieses "
            "Feld keine Auswirkungen."
        ),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ("-begin",)
        verbose_name = ugettext_lazy("Veranstaltung")
        verbose_name_plural = ugettext_lazy("Veranstaltungen")
        permissions = (
            (
                "can_see_hidden_events",
                ugettext_lazy("Darf nichtöffentliche Veranstaltungen sehen"),
            ),
        )

    def __str__(self):
        return " – ".join((localize(localtime(self.begin)), self.title))

    def get_absolute_url(self):
        if self.type in ("service", "prayer"):
            threshold = now() - datetime.timedelta(minutes=settings.THRESHOLD)
            if self.begin >= threshold:
                result = "{}#termin-{}".format(reverse("services"), self.pk)
            else:
                result = reverse("services")
        elif self.flat_page:
            result = self.flat_page.get_absolute_url()
        elif self.content:
            result = reverse(
                "single_event", args=[str(self.id)]
            )  # TODO: Check if this must be str(...)
        else:
            result = None
        return result

    @property
    def end(self):
        duration = self.duration or 0
        return self.begin + datetime.timedelta(minutes=duration)

    @property
    def time_sort(self):
        """
        Returns the timestamp that is used for sorting different types of
        objects that all appear on home view as article.
        """
        return self.begin

    def has_link_on_home(self):
        """
        Returns True if this instance has a link to another page on home view.
        """
        return (
            self.type in ("service", "prayer")
            or self.flat_page
            or (len(self.content) > settings.TRUNCATE_LENGTH)
        )

    def more_text(self):
        """
        Returns additional text for the home view.
        """
        template = Template(
            """
            <p>
                {{ coming_event.begin|date:"l, j. F Y, H:i" }}
                {% if coming_event.place %}
                    <br />{{ coming_event.place }}
                {% endif %}
            </p>
            {% if coming_event.content %}<p>{{ coming_event.content|truncatechars:TRUNCATE_LENGTH }}</p>{% endif %}
            """
        )
        return template.render(
            Context({"coming_event": self, "TRUNCATE_LENGTH": settings.TRUNCATE_LENGTH})
        )

    @property
    def fc_data(self):
        """
        Returns a string containing all data for the fullcalendar event object
        as JSON.
        """
        data = {
            "title": self.get_type_display() + ": " + self.title,
            "start": self.begin.isoformat(),
            "end": self.end.isoformat(),
            "color": EventTypes().event_types[self.type]["color"],
            "url": self.get_absolute_url(),
        }
        return json.dumps(data)

    @property
    def monthly_text(self):
        """
        Returns the model instance of the monthly text if this event is a
        service or a prayer.
        """
        result = None
        if self.type in ("service", "prayer"):
            for monthly_text in MonthlyText.objects.all():
                if (
                    monthly_text.datetime.year == self.begin.year
                    and monthly_text.datetime.month == self.begin.month
                ):
                    result = monthly_text
                    break
        return result


class AnnouncementManager(models.Manager):
    """
    Customized model manager to provide extra manager methods.
    """

    def get_coming_announcements(self):
        """
        Returns a special filtered and sorted list with coming announcements for
        home view and RSS feed.
        """
        coming_announcements_queryset = self.filter(end__gte=now()).reverse()
        coming_announcements = []
        for coming_announcement in coming_announcements_queryset:
            time_to_show = now() + datetime.timedelta(
                days=coming_announcement.on_home_before_end
            )
            if coming_announcement.end <= time_to_show:
                coming_announcements.append(coming_announcement)
        return coming_announcements


class Announcement(models.Model):
    """
    Model for announcements for home view.
    """

    objects = AnnouncementManager()

    title = models.CharField(
        ugettext_lazy("Titel"),
        max_length=255,
        help_text=ugettext_lazy("Kurzer Titel der Ankündigung."),
    )

    short_text = models.TextField(
        ugettext_lazy("Kurztext"),
        help_text=ugettext_lazy(
            "Kurzer Text. Erscheint auf der Startseite. Kein HTML erlaubt."
        ),
    )

    long_text = models.TextField(
        ugettext_lazy("Text"),
        blank=True,
        help_text=ugettext_lazy(
            "Längerer Text. Erscheint nur auf einer gesonderten Seite, die von "
            "der Startseite aus erreichbar ist. Kein HTML erlaubt. Leerzeilen "
            "können verwendet werden."
        ),
    )

    end = models.DateTimeField(
        ugettext_lazy("Ende"),
        help_text=ugettext_lazy(
            "Bis zu diesem Zeitpunkt ist die Ankündigung auf der Startseite "
            "und ggf. über den gesonderten Link erreichbar."
        ),
    )

    on_home_before_end = models.PositiveIntegerField(
        ugettext_lazy("Auf der Startseite (Angabe in Tagen)"),
        default=30,
        help_text=ugettext_lazy(
            "Die Ankündigung erscheint so viele Tage vor ihrem Ende auf der "
            "Startseite. Die Einstellung ermöglicht eine verzögerte "
            "Veröffentlichung."
        ),
    )

    mediafile = models.ForeignKey(
        verbose_name=ugettext_lazy("Bild"),
        to="MediaFile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ("-end",)
        verbose_name = ugettext_lazy("Ankündigung")
        verbose_name_plural = ugettext_lazy("Ankündigungen")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "announcement", args=[str(self.id)]
        )  # TODO: Check if this must be str(...)

    @property
    def time_sort(self):
        """
        Returns the timestamp that is used for sorting different types of
        objects that all appear on home view as article.
        """
        return self.end

    def has_link_on_home(self):
        """
        Returns True if this instance has a link to another page on home view.
        """
        return bool(self.long_text)

    def more_text(self):
        """
        Returns additional text for the home view.
        """
        template = Template("<p>{{ announcement.short_text }}</p>")
        return template.render(Context({"announcement": self}))


class MediaFile(models.Model):
    """
    Model for uploaded files like images.
    """

    mediafile = models.FileField(
        ugettext_lazy("Datei"),
        max_length=255,
        help_text=ugettext_lazy(
            "Achtung: Hochgeladene Dateien sind für jeden im Internet sichtbar."
        ),
    )

    text = models.TextField(
        ugettext_lazy("Alternativ-Text"),
        blank=True,
        help_text=ugettext_lazy(
            "Text, der als Alternativtext für Screenreader (Alt-Attribut) "
            "sowie als Tooltip (Title-Attribute) verwendet wird, wenn das Bild "
            "bei Veranstaltungen oder Ankündigungen eingebettet ist. Kein HTML "
            "erlaubt."
        ),
    )

    uploaded_on = models.DateTimeField(
        ugettext_lazy("Hochgeladen am"), auto_now_add=True
    )

    class Meta:
        ordering = ("-uploaded_on",)
        verbose_name = ugettext_lazy("Datei")
        verbose_name_plural = ugettext_lazy("Dateien")

    def __str__(self):
        return self.mediafile.url


class CurrentMarkusbote(models.Model):
    """
    Model for the current Markusbote. Can have zero or one instance.
    """

    file = models.ForeignKey(
        verbose_name=ugettext_lazy("Datei"),
        to=MediaFile,
        on_delete=models.PROTECT,
        help_text=ugettext_lazy(
            "Der aktuelle Markusbote muss zuerst hochgeladen werden. Dann "
            "steht er hier zur Auswahl."
        ),
    )

    months = models.CharField(
        ugettext_lazy("Monate"),
        max_length=255,
        help_text=ugettext_lazy("Beispiel: Oktober-November 2018"),
    )

    class Meta:
        verbose_name = ugettext_lazy("Aktueller Markusbote")
        verbose_name_plural = ugettext_lazy("Aktueller Markusbote")

    def __str__(self):
        return self.months

    def clean(self):
        """
        Throw ValidationError if you try to save more than one model
        instance. See: http://stackoverflow.com/a/6436008
        """
        model = self.__class__
        if model.objects.count() > 0 and self.id != model.objects.get().id:
            raise ValidationError(
                ugettext_lazy(
                    "Es kann gleichzeitig nur einen aktuellen Markusboten geben."
                )
            )


class ClericalWordAudioFile(models.Model):
    """
    Model for clerical word audio files.
    """

    file = models.FileField(
        ugettext_lazy("Audio-Datei"),
        max_length=255,
        help_text=ugettext_lazy(
            "Achtung: Hochgeladene Dateien sind für jeden im Internet sichtbar."
        ),
    )

    title = models.CharField(
        ugettext_lazy("Titel"),
        max_length=255,
        help_text=ugettext_lazy("Kurzer Titel des Beitrags."),
    )

    description = models.TextField(
        ugettext_lazy("Beschreibung des Beitrags"),
        blank=True,
        help_text=ugettext_lazy("Kein HTML erlaubt."),
    )

    mime_type = models.CharField(
        ugettext_lazy("MIME-Type (Internet Media Type)"),
        max_length=255,
        default="audio/mpeg",
        help_text=ugettext_lazy(
            "Dieser Wert ist ggf. an das Dateiformat anzupassen (z. B. in "
            "audio/mp4, audio/ogg, audio/wav)."
        ),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    pubdate = models.DateTimeField(
        ugettext_lazy("Veröffentlicht am"), auto_now_add=True
    )

    class Meta:
        ordering = ("-pubdate",)
        verbose_name = ugettext_lazy("Geistliches Wort Audio-Datei")
        verbose_name_plural = ugettext_lazy("Geistliches Wort Audio-Dateien")

    def __str__(self):
        return self.file.url
