from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_select_month(label, name, error_text=None, help_text=None, required=True, value=None):
    if error_text is None:
        error_text = {}

    context = (f'<div class="SelectInput{" required" if required else ""}">'
               f'<label class="fw-bold form-label" for={name}>{label}</label>'
               f'<select class="form-control{" is-invalid" if error_text else ""}" id="{name}" label="{label}" name="{name}">'
               f'<option value="">-- Select {label} --</option>'
               f'<option value="1"{" selected" if value == "1" else ""}>01 - January</option>'
               f'<option value="2"{" selected" if value == "2" else ""}>02 - February</option>'
               f'<option value="3"{" selected" if value == "3" else ""}>03 - March</option>'
               f'<option value="4"{" selected" if value == "4" else ""}>04 - April</option>'
               f'<option value="5"{" selected" if value == "5" else ""}>05 - May</option>'
               f'<option value="6"{" selected" if value == "6" else ""}>06 - June</option>'
               f'<option value="7"{" selected" if value == "7" else ""}>07 - July</option>'
               f'<option value="8"{" selected" if value == "8" else ""}>08 - August</option>'
               f'<option value="9"{" selected" if value == "9" else ""}>09 - September</option>'
               f'<option value="10"{" selected" if value == "10" else ""}>10 - October</option>'
               f'<option value="11"{" selected" if value == "11" else ""}>11 - November</option>'
               f'<option value="12"{" selected" if value == "12" else ""}>12 - December</option>'
               f'</select>')

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    if error_text:
        for error in error_text:
            context += f'<div class="help-message text-danger">{error}</div>'

    context += f'</div>'

    return mark_safe(context)
