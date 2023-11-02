import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.urls import reverse


class Command(BaseCommand):
    help = "Generate an Elm file that is used for the client component (implementation of the external church calendar"

    def handle(self, *args, **options):
        elm_file = ELM_FILE_TPL.format(
            staticPrefix=settings.STATIC_URL,
            service_url=reverse("services"),
            markusbote_url=reverse(
                "flat_page", kwargs={"category": "gemeinde", "page": "markusbote"}
            ),
            events_url=reverse("events"),
        )
        filename = os.path.abspath(os.path.join(__file__, "..", "..", "..", "external-calendar", "src", "Shared.elm"))
        with open(filename, "w") as f:
            f.write(elm_file)

        self.stdout.write(
            self.style.SUCCESS("Successfully created file {}".format(filename))
        )


ELM_FILE_TPL = """-- DO NOT EDIT: This is a generated file.


module Shared exposing (Urls, staticPrefix, urls)


staticPrefix : String
staticPrefix =
    "{staticPrefix}"


type alias Urls =
    {{ services : String
    , markusbote : String
    , events : String
    }}


urls : Urls
urls =
    Urls
        "{service_url}"
        "{markusbote_url}"
        "{events_url}"
"""
