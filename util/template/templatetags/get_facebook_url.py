from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_facebook_url():
    return settings.PUBLIC_FACEBOOK_URL
