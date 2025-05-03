from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_switch(label, name, help_text=None, value=None):
    context = (f'<div class="form-check form-switch">'
               f'<input class="form-check-input" id="{name}" {"checked" if value else ""} name="{name}" placeholder="{label}" type="checkbox">'
               f'<label class="fw-bold form-check-label" for={name}>{label}</label>')

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    context += f'</div>'

    return mark_safe(context)
