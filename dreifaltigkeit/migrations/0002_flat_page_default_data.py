# Generated by Django 2.0.6 on 2018-06-13 07:28

from django.conf import settings
from django.db import migrations


def add_flat_pages_parish(apps, schema_editor):
    """
    Adds all default flat pages for the parish site.
    """
    pages = (
        # Gemeinde
        ("gemeinde", "gruppen", "Gruppen und Kreise", 110, ""),
        ("gemeinde", "mitarbeiter-innen", "Mitarbeiter/innen", 120, ""),
        ("gemeinde", "kirchenvorstand", "Kirchenvorstand", 130, ""),
        ("gemeinde", "markusbote", "Markusbote", 140, ""),
        ("gemeinde", "schwestergemeinden", "Schwestergemeinden", 150, ""),
        ("gemeinde", "geschichte", "Geschichte", 160, ""),
        ("gemeinde", "gebaeude", "Gebäude", 170, ""),
        # Kirchenmusik
        ("kirchenmusik", "kantorei", "Kantorei", 210, ""),
        ("kirchenmusik", "markuschor", "Markuschor", 220, ""),
        ("kirchenmusik", "kurrende", "Kurrende", 230, ""),
        ("kirchenmusik", "posaunenchor", "Posaunenchor", 240, ""),
        ("kirchenmusik", "floetenkreis", "Flötenkreis", 250, ""),
        ("kirchenmusik", "konzerte", "Konzerte", 260, ""),
        ("kirchenmusik", "orgel", "Orgel", 270, ""),
        # Kinder und Jugend
        ("kinder-und-jugend", "krabbelkreis", "Krabbelkreis", 310, ""),
        ("kinder-und-jugend", "kurrende", "Kurrende", 320, "/kirchenmusik/kurrende/"),
        (
            "kinder-und-jugend",
            "kirche-fuer-kids",
            "Christenlehre / Kirche für Kids",
            330,
            "",
        ),
        (
            "kinder-und-jugend",
            "konfirmandenunterricht",
            "Konfirmandenunterricht",
            340,
            "",
        ),
        ("kinder-und-jugend", "junge-gemeinde", "Junge Gemeinde", 350, ""),
        ("kinder-und-jugend", "kindergarten", "Kindergarten", 360, ""),
        # Hauptmenü
        ("parish_root", "ehrenamt", "Ehrenamt", 410, ""),
        ("parish_root", "spenden", "Spenden / Kirchgeld", 420, ""),
        ("parish_root", "links", "Links", 430, ""),
    )

    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FlatPage = apps.get_model("dreifaltigkeit", "FlatPage")
    for category, url, title, ordering, redirect in pages:
        FlatPage.objects.create(
            category=category,
            url=url,
            title=title,
            ordering=ordering,
            redirect=redirect,
        )


def add_flat_pages_kindergarden(apps, schema_editor):
    """
    Adds all default flat pages for the kindergarden site.
    """
    pages = (
        # Hauptmenü
        ("kindergarden_root", "konzept", "Konzept", 110, ""),
        ("kindergarden_root", "mitarbeiter-innen", "Mitarbeiter/innen", 120, ""),
        ("kindergarden_root", "anmeldung", "Anmeldung eines Kindes", 130, ""),
        ("kindergarden_root", "termine", "Termine", 140, ""),
        ("kindergarden_root", "mitarbeit", "Mitarbeit und Unterstützung", 150, ""),
    )

    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FlatPage = apps.get_model("dreifaltigkeit", "FlatPage")
    for category, url, title, ordering, redirect in pages:
        FlatPage.objects.create(
            category=category,
            url=url,
            title=title,
            ordering=ordering,
            redirect=redirect,
        )


def add_flat_pages(apps, schema_editor):
    """
    Adds all default flat pages.
    """
    if settings.SITE_ID == "parish":
        add_flat_pages_parish(apps, schema_editor)
    elif settings.SITE_ID == "kindergarden":
        add_flat_pages_kindergarden(apps, schema_editor)
    else:
        raise RuntimeError(
            "The settings variable SITE_ID has to be set. Use 'parish' or "
            "'kindergarden'."
        )


class Migration(migrations.Migration):

    dependencies = [("dreifaltigkeit", "0001_initial")]

    operations = [migrations.RunPython(add_flat_pages)]
