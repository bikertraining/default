from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_business_phone(convert=False):
    if convert:
        return settings.PUBLIC_BUSINESS_PHONE.replace('-', '')
    else:
        return settings.PUBLIC_BUSINESS_PHONE
