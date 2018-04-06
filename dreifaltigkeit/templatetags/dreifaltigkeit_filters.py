from django import template


register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Filter to retrieve a value of a dictionary.
    """
    return dictionary.get(key)
