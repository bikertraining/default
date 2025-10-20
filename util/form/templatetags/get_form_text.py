from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_text(label, name, error_text=None, help_text=None, inputtype='text', is_cc=False, maxlength='256',
                  required=True, value=None):
    if error_text is None:
        error_text = {}

    context = (f'<div class="TextInput{" required" if required else ""}">'
               f'<label class="fw-bold form-label" for={name}>{label}</label>'
               f'<input class="form-control{" is-invalid" if error_text else ""}" id="{name}" name="{name}" maxlength="{maxlength}" placeholder="{label}" type="{inputtype}" value="{value}">')

    if is_cc:
        context += f'<img alt="Credit Card Types" class="mt-2" height="30" loading="lazy" src="{static("img/cc_types.webp")}" width="215"/>'

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    if error_text:
        for error in error_text:
            context += f'<div class="help-message text-danger">{error}</div>'

    context += f'</div>'

    return mark_safe(context)
