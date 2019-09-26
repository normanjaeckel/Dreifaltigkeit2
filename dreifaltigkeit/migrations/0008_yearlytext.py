# Generated by Django 2.0.6 on 2018-07-11 22:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("dreifaltigkeit", "0007_currentmarkusbote")]

    operations = [
        migrations.CreateModel(
            name="YearlyText",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "year",
                    models.IntegerField(
                        help_text="Eingabe als vierstellige Zahl.",
                        unique=True,
                        validators=[
                            django.core.validators.MinValueValidator(2018),
                            django.core.validators.MaxValueValidator(2199),
                        ],
                        verbose_name="Jahr",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text='Die Jahreslosung der <a href="https://www.oeab.de/">Ökumenischen Arbeitsgemeinschaft für Bibellesen</a> erscheint nur auf der Gottesdienstseite. Kein HTML erlaubt.',
                        verbose_name="Jahreslosung",
                    ),
                ),
                (
                    "verse",
                    models.CharField(
                        help_text="Beispiel: Joh 19,30.",
                        max_length=255,
                        verbose_name="Bibelstelle",
                    ),
                ),
            ],
            options={
                "verbose_name": "Jahreslosung",
                "verbose_name_plural": "Jahreslosungen",
                "ordering": ("-year",),
            },
        )
    ]
