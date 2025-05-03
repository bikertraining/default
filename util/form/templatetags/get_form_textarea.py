from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_textarea(label, name, error_text=None, help_text=None, required=True, rows='3', value=None):
    if error_text is None:
        error_text = {}

    context = (f'<div class="TextInput{" required" if required else ""}">'
               f'<label class="fw-bold form-label" for={name}>{label}</label>'
               f'<textarea class="form-control{" is-invalid" if error_text else ""}" id="{name}" name="{name}" placeholder="{label}" rows="{rows}">{value}</textarea>')

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    if error_text:
        for error in error_text:
            context += f'<div class="help-message text-danger">{error}</div>'

    context += f'</div>'

    return mark_safe(context)
