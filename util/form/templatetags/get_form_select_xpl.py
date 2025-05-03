from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_select_xpl(label, name, error_text=None, help_text=None, required=True, value=None):
    if error_text is None:
        error_text = {}

    context = (f'<div class="SelectInput{" required" if required else ""}">'
               f'<label class="fw-bold form-label" for={name}>{label}</label>'
               f'<select class="form-control{" is-invalid" if error_text else ""}" id="{name}" label="{label}" name="{name}">'
               f'<option value="none"{" selected" if value == "none" else ""}>None</option>'
               f'<option value="some"{" selected" if value == "some" else ""}>Some, but a long time ago</option>'
               f'<option value="1_6"{" selected" if value == "1_6" else ""}>1 to 6 months</option>'
               f'<option value="6_12"{" selected" if value == "6_12" else ""}>6 to 12 months</option>'
               f'<option value="more"{" selected" if value == "more" else ""}>More than one year</option>'
               f'<option value="dirt"{" selected" if value == "dirt" else ""}>Dirt bike only</option>'
               f'</select>')

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    if error_text:
        for error in error_text:
            context += f'<div class="help-message text-danger">{error}</div>'

    context += f'</div>'

    return mark_safe(context)
