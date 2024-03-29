from django import forms
from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy

from .models import (
    Announcement,
    ClericalWordAudioFile,
    CurrentMarkusbote,
    Event,
    FlatPage,
    MediaFile,
    MonthlyText,
    YearlyText,
)


class FlatPageAdmin(admin.ModelAdmin):
    class Media:
        css = {"all": ("assets/css/extra.css",)}

    # The next line is only for ordering of fields because we use readonly
    # fields.
    fields = (
        "category",
        "url",
        "title",
        "menu_title",
        "ordering",
        "redirect",
        "content",
    )

    readonly_fields = ("category", "url", "title", "menu_title", "ordering", "redirect")

    def has_add_permission(self, request):
        """
        Overridden permission check method to disable all create views for
        flat pages. New flat pages can only be added via command line.
        """
        return False


class EventAdminForm(forms.ModelForm):
    """
    This form is for custom validation of content field. If one uses markdown
    style links, these links should not overlap the position in the string
    according to TRUNCATE_LENGTH because then we can not truncate the string
    properly.
    """

    def clean_content(self):
        content = self.cleaned_data["content"]
        for match in settings.LINKIFY_REGEX.finditer(content):
            if (
                match.start() < settings.TRUNCATE_LENGTH - 1
                and match.end() >= settings.TRUNCATE_LENGTH
            ):
                raise ValidationError(
                    gettext(
                        "Ein Link in der Form [Text](URL) ist an der gegebenen "
                        "Stelle nicht zulässig. Bitte verschieben Sie den Link "
                        "im Text nach vorn oder hinten."
                    ),
                    code="linkify_error_bad_position",
                )
        return content


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = "begin"
    list_display = ("title", "place", "begin", "type", "on_home_before_begin")
    save_as = True
    save_as_continue = False
    form = EventAdminForm


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("__str__", "end")


class YearlyTextAdmin(admin.ModelAdmin):
    list_display = ("__str__", "text", "verse")


class MonthlyTextAdmin(admin.ModelAdmin):
    list_display = ("__str__", "text", "verse")


class MediaFileAdmin(admin.ModelAdmin):
    date_hierarchy = "uploaded_on"
    list_display = ("uploaded_on", "mediafile", "mediafile_url")

    # The next line is only for ordering of fields because we use readonly
    # fields.
    fields = ("mediafile", "text")

    def mediafile_url(self, obj):
        """
        Returns the URL to the uploaded file.
        """
        return obj.mediafile.url

    mediafile_url.short_description = gettext_lazy("Adresse (URL)")

    def get_readonly_fields(self, request, obj=None):
        """
        Hook for specifying custom readonly fields.

        If obj is None, we are in the create view. Here ere we want to edit the
        mediafile field to upload a new file. In the update (change) view we do
        not want this.
        """
        return ("mediafile",) if obj is not None else ()


class ClericalWordAudioFileAdmin(admin.ModelAdmin):
    date_hierarchy = "pubdate"
    list_display = ("title", "pubdate", "file", "file_url")

    # The next line is only for ordering of fields because we use readonly
    # fields.
    fields = ("file", "title", "description", "mediafile", "mime_type", "hidden")

    def file_url(self, obj):
        """
        Returns the URL to the uploaded file.
        """
        return obj.file.url

    file_url.short_description = gettext_lazy("Adresse (URL)")

    def get_readonly_fields(self, request, obj=None):
        """
        Hook for specifying custom readonly fields.

        If obj is None, we are in the create view. Here we want to edit the
        mediafile field to upload a new file. In the update (change) view we do
        not want this.
        """
        return ("file",) if obj is not None else ()


class CurrentMarkusboteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "mediafile_url")

    def mediafile_url(self, obj):
        """
        Returns the URL to the file.
        """
        return obj.file.mediafile.url

    mediafile_url.short_description = gettext_lazy("Adresse (URL)")

    def has_add_permission(self, request):
        """
        Don't allow addition of more than one model instance in Django admin.
        See: http://stackoverflow.com/a/12469482
        """
        return self.model.objects.count() == 0


admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(YearlyText, YearlyTextAdmin)
admin.site.register(MonthlyText, MonthlyTextAdmin)
admin.site.register(MediaFile, MediaFileAdmin)
admin.site.register(ClericalWordAudioFile, ClericalWordAudioFileAdmin)
admin.site.register(CurrentMarkusbote, CurrentMarkusboteAdmin)

description = gettext_lazy("{app_name} Administration").format(
    app_name=apps.get_app_config("dreifaltigkeit").verbose_name
)

site_instance = admin.site
site_instance.site_title = description
site_instance.site_header = description
