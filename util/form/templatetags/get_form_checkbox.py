from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_checkbox(label, name, error_text=None, help_text=None, required=True, value=None):
    if error_text is None:
        error_text = {}

    if value == 'on':
        value = False
    else:
        value = True

    context = (f'<div class="form-check{" required" if required else ""}">'
               f'<input class="border border-dark form-check-input{" is-invalid" if error_text else ""}" id="{name}" name="{name}" placeholder="{label}" type="checkbox" value="True"{" checked" if value else ""}>'
               f'<label class="fw-bold form-check-label" for={name}>{label}</label>')

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    if error_text:
        for error in error_text:
            context += f'<div class="help-message text-danger">{error}</div>'

    context += f'</div>'

    return mark_safe(context)
