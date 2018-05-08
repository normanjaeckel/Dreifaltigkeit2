# Generated by Django 2.0.2 on 2018-04-22 20:09

from django.db import migrations, models
import dreifaltigkeit.models


class Migration(migrations.Migration):

    dependencies = [
        ('dreifaltigkeit', '0008_monthlytext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlytext',
            name='month',
            field=models.IntegerField(help_text='Eingabe als sechsstellige Zahl bestehend aus Jahr und Monat z. B. 201307 für Juli 2013.', unique=True, validators=[dreifaltigkeit.models.validate_year_month_number], verbose_name='Monat'),
        ),
    ]