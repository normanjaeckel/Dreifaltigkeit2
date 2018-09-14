# Generated by Django 2.0.6 on 2018-09-14 16:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import dreifaltigkeit.models
import uuid


def add_flat_pages_parish(apps, schema_editor):
    """
    Adds all default flat pages for the parish site.
    """
    pages = (
        # Gemeinde
        ('gemeinde', 'gruppen', 'Gruppen und Kreise', '', 110, ''),
        ('gemeinde', 'mitarbeiter-innen', 'Mitarbeiter/innen', '', 120, ''),
        ('gemeinde', 'kirchenvorstand', 'Kirchenvorstand', '', 130, ''),
        ('gemeinde', 'markusbote', 'Markusbote', '', 140, ''),
        ('gemeinde', 'schwestergemeinden', 'Schwestergemeinden', '', 150, ''),
        ('gemeinde', 'geschichte', 'Geschichte', '', 160, ''),
        ('gemeinde', 'gebaeude', 'Gebäude', '', 170, ''),

        # Kirchenmusik
        ('kirchenmusik', 'kantorei', 'Kantorei', '', 210, ''),
        ('kirchenmusik', 'markuschor', 'Markuschor', '', 220, ''),
        ('kirchenmusik', 'kurrende', 'Kurrende und Vorkurrende', 'Kurrende', 230, ''),
        ('kirchenmusik', 'posaunenchor', 'Posaunenchor', '', 240, ''),
        ('kirchenmusik', 'konzerte', 'Konzerte', '', 250, ''),
        ('kirchenmusik', 'orgel', 'Orgel', '', 260, ''),

        # Kinder und Jugend
        ('kinder-und-jugend', 'krabbelkreis', 'Krabbelkreis', '', 310, ''),
        ('kinder-und-jugend', 'kurrende', 'Kurrende', '', 320, '/kirchenmusik/kurrende/'),
        ('kinder-und-jugend', 'kirche-fuer-kids', 'Kirche für Kids (Christenlehre)', '', 330, ''),
        ('kinder-und-jugend', 'konfirmandenunterricht', 'Konfirmandenunterricht', '', 340, ''),
        ('kinder-und-jugend', 'junge-gemeinde', 'Junge Gemeinde', '', 350, ''),
        ('kinder-und-jugend', 'kindergarten', 'Kindergarten', '', 360, settings.LINK_TO_OTHER_SITE),

        # Hauptmenü
        ('parish_root', 'ehrenamt', 'Ehrenamt', '', 410, ''),
        ('parish_root', 'spenden', 'Spenden / Kirchgeld', '', 420, ''),
        ('parish_root', 'links', 'Links', '', 430, ''),
    )

    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FlatPage = apps.get_model('dreifaltigkeit', 'FlatPage')
    for category, url, title, menu_title, ordering, redirect in pages:
        FlatPage.objects.create(
            category=category,
            url=url,
            title=title,
            menu_title=menu_title,
            ordering=ordering,
            redirect=redirect,
        )


def add_flat_pages_kindergarden(apps, schema_editor):
    """
    Adds all default flat pages for the kindergarden site.
    """
    pages = (
        # Hauptmenü
        ('kindergarden_root', 'konzept', 'Pädagogisches Konzept', 'Konzept', 110, ''),
        ('kindergarden_root', 'mitarbeiter-innen', 'Mitarbeiter/innen', '', 120, ''),
        ('kindergarden_root', 'anmeldung', 'Anmeldung eines Kindes', '', 130, ''),
        ('kindergarden_root', 'termine', 'Termine', '', 140, ''),
        ('kindergarden_root', 'mitarbeit', 'Mitarbeit und Unterstützung', '', 150, ''),
    )

    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FlatPage = apps.get_model('dreifaltigkeit', 'FlatPage')
    for category, url, title, menu_title, ordering, redirect in pages:
        FlatPage.objects.create(
            category=category,
            url=url,
            title=title,
            menu_title=menu_title,
            ordering=ordering,
            redirect=redirect,
        )


def add_flat_pages(apps, schema_editor):
    """
    Adds all default flat pages.
    """
    if settings.SITE_ID == 'parish':
        add_flat_pages_parish(apps, schema_editor)
    elif settings.SITE_ID == 'kindergarden':
        add_flat_pages_kindergarden(apps, schema_editor)
    else:
        raise RuntimeError(
            "The settings variable SITE_ID has to be set. Use 'parish' or "
            "'kindergarden'.")


class Migration(migrations.Migration):

    replaces = [('dreifaltigkeit', '0001_initial'), ('dreifaltigkeit', '0002_flat_page_default_data'), ('dreifaltigkeit', '0003_flatpage_menu_title'), ('dreifaltigkeit', '0004_announcement_mediafile'), ('dreifaltigkeit', '0005_auto_20180711_1452'), ('dreifaltigkeit', '0006_flat_page_default_data_change'), ('dreifaltigkeit', '0007_currentmarkusbote'), ('dreifaltigkeit', '0008_yearlytext'), ('dreifaltigkeit', '0009_flat_page_delete_floetenkreis'), ('dreifaltigkeit', '0010_auto_20180830_2205'), ('dreifaltigkeit', '0011_flat_page_default_data_change'), ('dreifaltigkeit', '0012_auto_20180912_2230')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Kurzer Titel der Ankündigung.', max_length=255, verbose_name='Titel')),
                ('short_text', models.TextField(help_text='Kurzer Text. Erscheint auf der Startseite. Kein HTML erlaubt.', verbose_name='Kurztext')),
                ('long_text', models.TextField(blank=True, help_text='Längerer Text. Erscheint nur auf einer gesonderten Seite, die von der Startseite aus erreichbar ist. Kein HTML erlaubt. Leerzeilen können verwendet werden.', verbose_name='Text')),
                ('end', models.DateTimeField(help_text='Bis zu diesem Zeitpunkt ist die Ankündigung auf der Startseite und ggf. über den gesonderten Link erreichbar.', verbose_name='Ende')),
            ],
            options={
                'verbose_name': 'Ankündigung',
                'verbose_name_plural': 'Ankündigungen',
                'ordering': ('-end',),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('service', 'Gottesdienst'), ('prayer', 'Andacht'), ('concert', 'Konzert'), ('gathering', 'Treff'), ('period-of-reflection', 'Rüstzeit'), ('default', 'Sonstige Veranstaltung'), ('hidden', 'Nichtöffentliche Veranstaltung')], default='default', help_text='Gottesdienste und Konzerte werden auf den besonderen Seite zusätzlich angezeigt.', max_length=255, verbose_name='Veranstaltungstyp')),
                ('title', models.CharField(help_text='Kurzer Titel der Veranstaltung.', max_length=255, verbose_name='Titel')),
                ('place', models.CharField(blank=True, default='Trinitatiskirche', help_text='Ort der Veranstaltung, z. B. Trinitatiskirche, Markuskapelle, Anbau der Trinitatiskirche, Gemeindehaus Dresdner Straße 59.', max_length=255, verbose_name='Ort')),
                ('content', models.TextField(blank=True, help_text='Beschreibung der Veranstaltung. Kein HTML erlaubt.', verbose_name='Inhalt')),
                ('begin', models.DateTimeField(verbose_name='Beginn')),
                ('duration', models.PositiveIntegerField(blank=True, help_text='Wenn nichts angegeben ist, wird keine Zeit für das Ende der Veranstaltung angezeigt.', null=True, verbose_name='Dauer in Minuten')),
                ('on_home_before_begin', models.PositiveIntegerField(default=0, help_text='Die Veranstaltung erscheint so viele Tage vor Beginn auf der Startseite. Wählen Sie 0, wenn die Veranstaltung niemals auf der Startseite erscheinen soll. Der nächste Gottesdienste und das nächste Konzert erscheinen immer auf der Startseite, egal, was hier eingestellt ist.', verbose_name='Auf der Startseite (in Tagen)')),
            ],
            options={
                'verbose_name': 'Veranstaltung',
                'verbose_name_plural': 'Veranstaltungen',
                'ordering': ('-begin',),
                'permissions': (('can_see_hidden_events', 'Darf nichtöffentliche Veranstaltungen sehen'),),
            },
        ),
        migrations.CreateModel(
            name='FlatPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('gemeinde', 'Gemeinde'), ('kirchenmusik', 'Kirchenmusik'), ('kinder-und-jugend', 'Kinder und Jugend'), ('parish_root', 'Gemeinde Hauptmenü'), ('kindergarden_root', 'Kindergarten Hauptmenü')], max_length=255, verbose_name='Kategorie')),
                ('url', models.CharField(max_length=255, verbose_name='URL')),
                ('title', models.CharField(max_length=255, verbose_name='Titel')),
                ('ordering', models.IntegerField(verbose_name='Sortierung')),
                ('redirect', models.CharField(blank=True, help_text='Wenn eine Weiterleitung eingerichtet ist, wird kein zusätzlicher Inhalt angezeigt.', max_length=255, verbose_name='Weiterleitung')),
                ('content', models.TextField(blank=True, default='<p>\n\n\n\n</p>', help_text='Inhalt der Seite in HTML.', verbose_name='Inhalt')),
            ],
            options={
                'verbose_name': 'Statische Seite',
                'verbose_name_plural': 'Statische Seiten',
                'ordering': ('ordering',),
            },
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mediafile', models.FileField(help_text='Achtung: Hochgeladene Dateien sind für jeden im Internet sichtbar.', max_length=255, upload_to='', verbose_name='Datei')),
                ('uploaded_on', models.DateTimeField(auto_now_add=True, verbose_name='Hochgeladen am')),
            ],
            options={
                'verbose_name': 'Datei',
                'verbose_name_plural': 'Dateien',
                'ordering': ('-uploaded_on',),
            },
        ),
        migrations.CreateModel(
            name='MonthlyText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(help_text='Eingabe als sechsstellige Zahl bestehend aus Jahr und Monat z. B. 201307 für Juli 2013.', unique=True, validators=[dreifaltigkeit.models.validate_year_month_number], verbose_name='Monat')),
                ('text', models.TextField(help_text='Der Monatsspruch der <a href="https://www.oeab.de/">Ökumenischen Arbeitsgemeinschaft für Bibellesen</a> erscheint nur auf der Gottesdienstseite. Kein HTML erlaubt.', verbose_name='Monatsspruch')),
                ('verse', models.CharField(help_text='Beispiel: Joh 19,30.', max_length=255, verbose_name='Bibelstelle')),
            ],
            options={
                'verbose_name': 'Monatsspruch',
                'verbose_name_plural': 'Monatssprüche',
                'ordering': ('-month',),
            },
        ),
        migrations.AddField(
            model_name='flatpage',
            name='menu_title',
            field=models.CharField(blank=True, help_text='Wenn hier nichts eingetragen ist, wird der Titel zugleich als Bezeichnung im Menü verwendet.', max_length=255, verbose_name='Eintrag im Menü'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='mediafile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dreifaltigkeit.MediaFile', verbose_name='Bild'),
        ),
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.PositiveIntegerField(blank=True, help_text='Wenn nichts angegeben ist, wird keine Zeit für das Ende der Veranstaltung angezeigt.', null=True, verbose_name='Dauer (Angabe in Minuten)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='on_home_before_begin',
            field=models.PositiveIntegerField(default=0, help_text='Die Veranstaltung erscheint so viele Tage vor Beginn auf der Startseite. Wählen Sie 0, wenn die Veranstaltung niemals auf der Startseite erscheinen soll. Der nächste Gottesdienste und das nächste Konzert erscheinen immer auf der Startseite, egal, was hier eingestellt ist.', verbose_name='Auf der Startseite (Angabe in Tagen)'),
        ),
        migrations.CreateModel(
            name='CurrentMarkusbote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('months', models.CharField(help_text='Beispiel: Oktober-November 2018', max_length=255, verbose_name='Monate')),
                ('file', models.ForeignKey(help_text='Der aktuelle Markusbote muss zuerst hochgeladen werden. Dann steht er hier zur Auswahl.', on_delete=django.db.models.deletion.PROTECT, to='dreifaltigkeit.MediaFile', verbose_name='Datei')),
            ],
            options={
                'verbose_name': 'Aktueller Markusbote',
                'verbose_name_plural': 'Aktueller Markusbote',
            },
        ),
        migrations.CreateModel(
            name='YearlyText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(help_text='Eingabe als vierstellige Zahl.', unique=True, validators=[django.core.validators.MinValueValidator(2018), django.core.validators.MaxValueValidator(2199)], verbose_name='Jahr')),
                ('text', models.TextField(help_text='Die Jahreslosung der <a href="https://www.oeab.de/">Ökumenischen Arbeitsgemeinschaft für Bibellesen</a> erscheint nur auf der Gottesdienstseite. Kein HTML erlaubt.', verbose_name='Jahreslosung')),
                ('verse', models.CharField(help_text='Beispiel: Joh 19,30.', max_length=255, verbose_name='Bibelstelle')),
            ],
            options={
                'verbose_name': 'Jahreslosung',
                'verbose_name_plural': 'Jahreslosungen',
                'ordering': ('-year',),
            },
        ),
        migrations.AddField(
            model_name='announcement',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='event',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='event',
            name='for_kids',
            field=models.BooleanField(default=False, help_text='Nur bei Gottesdiensten kann hier eingestellt werden, ob das Kindergottesdienst-Logo angezeigt werden soll. Sonst hat dieses Feld keine Auswirkungen.', verbose_name='Gottesdienst mit Kindergottesdienst'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('service', 'Gottesdienst'), ('prayer', 'Andacht'), ('concert', 'Konzert'), ('gathering', 'Treff'), ('period-of-reflection', 'Rüstzeit'), ('default', 'Sonstige Veranstaltung'), ('hidden', 'Nichtöffentliche Veranstaltung')], default='default', help_text='Gottesdienste und Andachten werden auf der besonderen Seite zusätzlich angezeigt.', max_length=255, verbose_name='Veranstaltungstyp'),
        ),
        migrations.RunPython(
            add_flat_pages,
        ),
    ]
