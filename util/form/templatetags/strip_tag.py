from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def strip_tag(name, value=None, first=0, last=0):
    context = name[first:-last]

    return mark_safe(context)
