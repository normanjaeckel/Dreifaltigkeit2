# Generated by Django 2.2.5 on 2022-11-04 19:30

from django.conf import settings
from django.db import migrations


def change_flat_pages(apps, schema_editor):
    """
    Changes one parish flat page.
    """
    if settings.SITE_ID == "parish":
        # We can't import the model directly as it may be a newer
        # version than this migration expects. We use the historical version.
        FlatPage = apps.get_model("dreifaltigkeit", "FlatPage")

        flat_page_1 = FlatPage.objects.get(
            category="kinder-und-jugend", url="kirche-fuer-kids"
        )
        flat_page_1.title = "Kinderkirche"
        flat_page_1.menu_title = "Kinderkirche"
        flat_page_1.save()
    elif settings.SITE_ID == "kindergarden":
        pass
    else:
        raise RuntimeError(
            "The settings variable SITE_ID has to be set. Use 'parish' or "
            "'kindergarden'."
        )


class Migration(migrations.Migration):

    dependencies = [
        ("dreifaltigkeit", "0016_flat_page_change_christenlehre_20210903_1340")
    ]

    operations = [migrations.RunPython(change_flat_pages)]
