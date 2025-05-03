from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_instagram_url():
    return settings.PUBLIC_INSTAGRAM_URL
