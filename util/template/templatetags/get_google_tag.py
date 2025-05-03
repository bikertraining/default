from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_google_tag():
    return settings.PUBLIC_GOOGLE_TAG
