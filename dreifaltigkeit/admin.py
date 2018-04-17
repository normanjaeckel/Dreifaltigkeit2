from django.apps import apps
from django.contrib import admin
from django.utils.translation import ugettext_lazy

from .models import Announcement, Event, MediaFile


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'place', 'begin', 'type', )


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'end', )


admin.site.register(Event, EventAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(MediaFile)

description = ugettext_lazy('{app_name} Administration').format(
    app_name=apps.get_app_config('dreifaltigkeit').verbose_name)

site_instance = admin.site
site_instance.site_title = description
site_instance.site_header = description
