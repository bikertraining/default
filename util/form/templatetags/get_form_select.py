from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_select(label, name, error_text=None, help_text=None, options=None, required=True, value=None):
    if error_text is None:
        error_text = {}

    if options is None:
        options = {}

    context = (f'<div class="SelectInput{" required" if required else ""}">'
               f'<label class="fw-bold form-label" for={name}>{label}</label>'
               f'<select class="form-control{" is-invalid" if error_text else ""}" id="{name}" label="{label}" name="{name}">'
               f'<option value="">-- Select {label} --</option>')

    for key, values in options:
        context += f'<option value="{key}"{" selected" if key == value else ""}>{values}</option>'

    context += f'</select>'

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    if error_text:
        for error in error_text:
            context += f'<div class="help-message text-danger">{error}</div>'

    context += f'</div>'

    return mark_safe(context)
