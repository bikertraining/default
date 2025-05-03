from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_brp_url():
    return settings.PUBLIC_BRP_URL
