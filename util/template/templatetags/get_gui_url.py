from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_gui_url():
    return settings.PUBLIC_GUI_URL
