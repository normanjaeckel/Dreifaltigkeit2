# Generated by Django 2.2.12 on 2020-04-10 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dreifaltigkeit", "0013_clericalwordaudiofile_hidden"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="content",
            field=models.TextField(
                blank=True,
                help_text="Beschreibung der Veranstaltung. Kein HTML erlaubt. Links im Markdown-Stil sind mit Einschränkungen möglich, d. h. [Text](URL).",
                verbose_name="Inhalt",
            ),
        ),
    ]
