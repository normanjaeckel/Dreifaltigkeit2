# Generated by Django 2.0.2 on 2018-04-11 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dreifaltigkeit', '0003_auto_20180411_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('service', 'Gottesdienst'), ('prayer', 'Andacht'), ('concert', 'Konzert'), ('gathering', 'Treff'), ('period-of-reflection', 'Rüstzeit'), ('default', 'Sonstige Veranstaltung'), ('hidden', 'Nichtöffentliche Veranstaltung')], default='default', help_text='Gottesdienste und Konzerte werden auf den besonderen Seite zusätzlich angezeigt.', max_length=255, verbose_name='Veranstaltungstyp'),
        ),
    ]