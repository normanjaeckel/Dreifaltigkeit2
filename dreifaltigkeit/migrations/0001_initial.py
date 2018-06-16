# Generated by Django 2.0.6 on 2018-06-16 16:55

from django.db import migrations, models
import dreifaltigkeit.models


class Migration(migrations.Migration):

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
    ]
