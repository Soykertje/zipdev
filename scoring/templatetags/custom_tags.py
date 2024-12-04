from django import template

register = template.Library()


@register.filter
def attr(obj, attr_name):
    """
    Returns the attribute of an object, or None if it doesn't exist.
    """
    return getattr(obj, attr_name, None)
