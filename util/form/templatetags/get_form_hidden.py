from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_hidden(name, value=None):
    context = f'<input id="{name}" name="{name}" type="hidden" value="{value}">'

    return mark_safe(context)
