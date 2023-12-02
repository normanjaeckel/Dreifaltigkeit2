import json

from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView

from .models import (
    Announcement,
    ClericalWordAudioFile,
    CurrentMarkusbote,
    MonthlyText,
    YearlyText,
)
from .models import FlatPage as FlatPageModel


class Home(TemplateView):
    """
    Home view.
    """

    def get_template_names(self):
        """
        Returns the template name: home_parish.html or home_kindergarden.html.
        """
        return ["home_{}.html".format(settings.SITE_ID)]

    def get_context_data(self, **context):
        try:
            yearly_text = YearlyText.objects.get(year=timezone.now().year)
        except YearlyText.DoesNotExist:
            yearly_text = None

        try:
            current_markusbote = CurrentMarkusbote.objects.get()
        except CurrentMarkusbote.DoesNotExist:
            current_markusbote = None

        announcements = []
        for a in Announcement.objects.get_coming_announcements():
            announcement = {
                "title": a.title,
                "short_text": a.short_text,
                "link": a.get_absolute_url(),
                "end": a.end.isoformat(),
            }
            if a.mediafile:
                announcement["image"] = {
                    "src": a.mediafile.mediafile.url,
                    "text": a.mediafile.text,
                }
            announcements.append(announcement)

        return super().get_context_data(
            yearly_text=yearly_text,
            current_markusbote=current_markusbote,
            announcements=json.dumps(announcements),
            announcements_django=Announcement.objects.get_coming_announcements(),
            **context
        )


class Services(TemplateView):
    """
    View for all services
    """

    template_name = "services.html"

    def get_context_data(self, **context):
        monthly_texts = [
            {"month": t.month, "text": t.text, "verse": t.verse}
            for t in MonthlyText.objects.all()
        ]
        return super().get_context_data(
            monthly_texts=json.dumps(monthly_texts), **context
        )


class ClericalWordPage(ListView):
    """
    View for all clerical word audio files.
    """

    queryset = ClericalWordAudioFile.objects.all().exclude(hidden=True)
    template_name = "clerical_word.html"


class Events(TemplateView):
    """
    View for all events.
    """

    template_name = "events.html"


class SingleEvent(TemplateView):
    """
    View for a single event.
    """

    template_name = "single_event.html"


class FlatPage(TemplateView):
    """
    View for all root and non-root flat pages.
    """

    root = False
    template_name = "flat_page.html"

    def get_context_data(self, *args, **kwargs):
        """
        Customized method: Adds flat page instance to the context and sends
        HTTP 404 if page does not exist.
        """
        context = super().get_context_data(*args, **kwargs)
        if self.root:
            category = "{}_root".format(settings.SITE_ID)
        else:
            category = context["category"]
        context["flat_page"] = get_object_or_404(
            FlatPageModel, category=category, url=context["page"]
        )
        return context

    def get(self, request, *args, **kwargs):
        """
        Overridden method. Returns HTTP 301 if flat page is only for redirect.
        """
        context = self.get_context_data(**kwargs)
        if context["flat_page"].redirect:
            return HttpResponsePermanentRedirect(context["flat_page"].redirect)
        return self.render_to_response(context)


class Imprint(TemplateView):
    """
    Imprint view with legal information.
    """

    template_name = "imprint.html"


class Announcements(DetailView):
    """
    View for details of an announcement.
    """

    template_name = "announcements.html"
    model = Announcement

    def get_object(self):
        """
        Customized method: Send HTTP 404 if time is elapsed or if there is
        no long_text.
        """
        announcement = super().get_object()
        if announcement.end < timezone.now() or not announcement.long_text:
            message = "Announcement {} is elapsed or has no long_text.".format(
                announcement.title
            )
            raise Http404(message)
        return announcement


class SpecialPage(TemplateView):
    """
    Prepared class for special pages. Use flat page template and customized it.
    """

    pass
