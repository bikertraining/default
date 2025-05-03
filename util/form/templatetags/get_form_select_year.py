from datetime import date

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_select_year(label, name, error_text=None, help_text=None, required=True, value=None):
    if error_text is None:
        error_text = {}

    context = (f'<div class="SelectInput{" required" if required else ""}">'
               f'<label class="fw-bold form-label" for={name}>{label}</label>'
               f'<select class="form-control{" is-invalid" if error_text else ""}" id="{name}" label="{label}" name="{name}">'
               f'<option value="">-- Select {label} --</option>')

    today = date.today().year

    for year in range(today, today + 10):
        context += f'<option value="{year}"{" selected" if str(year) == str(value) else ""}>{year}</option>'

    context += f'</select>'

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    if error_text:
        for error in error_text:
            context += f'<div class="help-message text-danger">{error}</div>'

    context += f'</div>'

    return mark_safe(context)
