# Generated by Django 2.0.2 on 2018-05-08 20:21

from django.db import migrations


def add_flatpages(apps, schema_editor):
    """
    Adds all default flatpages.
    """
    pages = (
        # Gemeinde
        ('gemeinde', 'gruppen', 'Gruppen und Kreise', 110, ''),
        ('gemeinde', 'mitarbeiter-innen', 'Mitarbeiter/innen', 120, ''),
        ('gemeinde', 'kirchenvorstand', 'Kirchenvorstand', 130, ''),
        ('gemeinde', 'markusbote', 'Markusbote', 140, ''),
        ('gemeinde', 'schwestergemeinden', 'Schwestergemeinden', 150, ''),
        ('gemeinde', 'geschichte', 'Geschichte', 160, ''),
        ('gemeinde', 'gebaeude', 'Gebäude', 170, ''),

        # Kirchenmusik
        ('kirchenmusik', 'kantorei', 'Kantorei', 210, ''),
        ('kirchenmusik', 'markuschor', 'Markuschor', 220, ''),
        ('kirchenmusik', 'kurrende', 'Kurrende', 230, ''),
        ('kirchenmusik', 'posaunenchor', 'Posaunenchor', 240, ''),
        ('kirchenmusik', 'floetenkreis', 'Flötenkreis', 250, ''),
        ('kirchenmusik', 'konzerte', 'Konzerte', 260, ''),
        ('kirchenmusik', 'orgel', 'Orgel', 270, ''),

        # Kinder und Jugend
        ('kinder-und-jugend', 'krabbelkreis', 'Krabbelkreis', 310, ''),
        ('kinder-und-jugend', 'kurrende', 'Kurrende', 320, '/kirchenmusik/kurrende/'),
        ('kinder-und-jugend', 'kirche-fuer-kids', 'Christenlehre / Kirche für Kids', 330, ''),
        ('kinder-und-jugend', 'konfirmandenunterricht', 'Konfirmandenunterricht', 340, ''),
        ('kinder-und-jugend', 'junge-gemeinde', 'Junge Gemeinde', 350, ''),
        ('kinder-und-jugend', 'kindergarten', 'Kindergarten', 360, ''),
    )

    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FlatPage = apps.get_model('dreifaltigkeit', 'FlatPage')
    for category, url, title, ordering, redirect in pages:
        FlatPage.objects.create(
            category=category,
            url=url,
            title=title,
            ordering=ordering,
            redirect=redirect,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('dreifaltigkeit', '0011_flatpage_redirect'),
    ]

    operations = [
        migrations.RunPython(add_flatpages),
    ]
