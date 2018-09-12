from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def possibly_active(context, category):
    """
    Returns CSS class 'active' for submenu if the respective path is
    requested. E. g. Request path '/gemeinde/foo/bar' returns 'active' for
    category 'gemeinde'.
    """
    if context.request.path.startswith('/' + category):
        return 'active'
