import re

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

regex = re.compile(r"https?://\S+")

@register.filter(needs_autoescape=True)
@stringfilter
def linkify(value, autoescape=True):
    """
    Adds a tag to http or https URL.
    """

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    value = esc(value)

    def replace(link):
        return f'<a href="{link.group(0)}">{link.group(0)}</a>'

    result = regex.sub(replace, value)
    return mark_safe(result)
