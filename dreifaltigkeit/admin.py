from django.apps import apps
from django.contrib import admin
from django.utils.translation import ugettext_lazy

from .models import Announcement, Event, FlatPage, MediaFile, MonthlyText


class FlatPageAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('assets/css/extra.css',)
        }

    fields =  ('category', 'url', 'title', 'menu_title', 'ordering', 'redirect', 'content',)
    readonly_fields = ('category', 'url', 'title', 'menu_title', 'ordering', 'redirect',)

    def has_add_permission(self, request):
        """
        Overridden permission check method to disable all create views for
        flat pages. New flat pages can only be added via command line.
        """
        return False


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'begin'
    list_display = ('title', 'place', 'begin', 'type', )
    save_as = True
    save_as_continue = False


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'end', )


class MonthlyTextAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'text', 'verse', )


class MediaFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'uploaded_on'
    list_display = ('mediafile', 'uploaded_on', 'mediafile_url', )

    def mediafile_url(self, obj):
        """
        Returns the URL to the uploaded file.
        """
        return obj.mediafile.url
    mediafile_url.short_description = ugettext_lazy('Adresse (URL)')

    def has_change_permission(self, request, obj=None):
        """
        Returns the default value (True) if obj is None else False. This
        indicates editing of objects of this type is permitted in general
        but not for (every) specific object. This way we get the admin list
        view but not the update (change) views.
        """
        if obj is not None:
            return False
        return super().has_change_permission(request, obj)


admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(MonthlyText, MonthlyTextAdmin)
admin.site.register(MediaFile, MediaFileAdmin)

description = ugettext_lazy('{app_name} Administration').format(
    app_name=apps.get_app_config('dreifaltigkeit').verbose_name)

site_instance = admin.site
site_instance.site_title = description
site_instance.site_header = description
