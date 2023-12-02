from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
@stringfilter
def linkify(value, autoescape=True):
    """
    Adds an anchor tag to URL marked in markdown style.
    """

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    value = esc(value)

    def replace(link):
        return f'<a href="{link.group(2)}">{link.group(1)}</a>'

    result = settings.LINKIFY_REGEX.sub(replace, value)
    return mark_safe(result)
