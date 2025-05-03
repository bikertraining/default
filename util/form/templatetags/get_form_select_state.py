from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_select_state(label, name, error_text=None, help_text=None, required=True, value=None):
    if error_text is None:
        error_text = {}

    context = (f'<div class="SelectInput{" required" if required else ""}">'
               f'<label class="fw-bold form-label" for={name}>{label}</label>'
               f'<select class="form-control{" is-invalid" if error_text else ""}" id="{name}" label="{label}" name="{name}">'
               f'<option value="">-- Select State --</option>'
               f'<option value="AL"{" selected" if value == "AL" else ""}>Alabama</option>'
               f'<option value="AK"{" selected" if value == "AK" else ""}>Alaska</option>'
               f'<option value="AZ"{" selected" if value == "AZ" else ""}>Arizona</option>'
               f'<option value="AR"{" selected" if value == "AR" else ""}>Arkansas</option>'
               f'<option value="CA"{" selected" if value == "CA" else ""}>California</option>'
               f'<option value="CO"{" selected" if value == "CO" else ""}>Colorado</option>'
               f'<option value="CT"{" selected" if value == "CT" else ""}>Connecticut</option>'
               f'<option value="DE"{" selected" if value == "DE" else ""}>Delaware</option>'
               f'<option value="DC"{" selected" if value == "DC" else ""}>District of Columbia</option>'
               f'<option value="FL"{" selected" if value == "FL" else ""}>Florida</option>'
               f'<option value="GA"{" selected" if value == "GA" else ""}>Georgia</option>'
               f'<option value="HI"{" selected" if value == "HI" else ""}>Hawaii</option>'
               f'<option value="ID"{" selected" if value == "ID" else ""}>Idaho</option>'
               f'<option value="IL"{" selected" if value == "IL" else ""}>Illinois</option>'
               f'<option value="IN"{" selected" if value == "IN" else ""}>Indiana</option>'
               f'<option value="IA"{" selected" if value == "IA" else ""}>Iowa</option>'
               f'<option value="KS"{" selected" if value == "KS" else ""}>Kansas</option>'
               f'<option value="KY"{" selected" if value == "KY" else ""}>Kentucky</option>'
               f'<option value="LA"{" selected" if value == "LA" else ""}>Louisiana</option>'
               f'<option value="ME"{" selected" if value == "ME" else ""}>Maine</option>'
               f'<option value="MD"{" selected" if value == "MD" else ""}>Maryland</option>'
               f'<option value="MA"{" selected" if value == "MA" else ""}>Massachusetts</option>'
               f'<option value="MI"{" selected" if value == "MI" else ""}>Michigan</option>'
               f'<option value="MN"{" selected" if value == "MN" else ""}>Minnesota</option>'
               f'<option value="MS"{" selected" if value == "MS" else ""}>Mississippi</option>'
               f'<option value="MO"{" selected" if value == "MO" else ""}>Missouri</option>'
               f'<option value="MT"{" selected" if value == "MT" else ""}>Montana</option>'
               f'<option value="NE"{" selected" if value == "NE" else ""}>Nebraska</option>'
               f'<option value="NV"{" selected" if value == "NV" else ""}>Nevada</option>'
               f'<option value="NH"{" selected" if value == "NH" else ""}>New Hampshire</option>'
               f'<option value="NJ"{" selected" if value == "NJ" else ""}>New Jersey</option>'
               f'<option value="NM"{" selected" if value == "NM" else ""}>New Mexico</option>'
               f'<option value="NY"{" selected" if value == "NY" else ""}>New York</option>'
               f'<option value="NC"{" selected" if value == "NC" else ""}>North Carolina</option>'
               f'<option value="ND"{" selected" if value == "ND" else ""}>North Dakota</option>'
               f'<option value="OH"{" selected" if value == "OH" else ""}>Ohio</option>'
               f'<option value="OK"{" selected" if value == "OK" else ""}>Oklahoma</option>'
               f'<option value="OR"{" selected" if value == "OR" else ""}>Oregon</option>'
               f'<option value="PA"{" selected" if value == "PA" else ""}>Pennsylvania</option>'
               f'<option value="RI"{" selected" if value == "RI" else ""}>Rhode Island</option>'
               f'<option value="SC"{" selected" if value == "SC" else ""}>South Carolina</option>'
               f'<option value="SD"{" selected" if value == "SD" else ""}>South Dakota</option>'
               f'<option value="TN"{" selected" if value == "TN" else ""}>Tennessee</option>'
               f'<option value="TX"{" selected" if value == "TX" else ""}>Texas</option>'
               f'<option value="UT"{" selected" if value == "UT" else ""}>Utah</option>'
               f'<option value="VT"{" selected" if value == "VT" else ""}>Vermont</option>'
               f'<option value="VA"{" selected" if value == "VA" else ""}>Virginia</option>'
               f'<option value="WA"{" selected" if value == "WA" else ""}>Washington</option>'
               f'<option value="WV"{" selected" if value == "WV" else ""}>West Virginia</option>'
               f'<option value="WI"{" selected" if value == "WI" else ""}>Wisconsin</option>'
               f'<option value="WY"{" selected" if value == "WY" else ""}>Wyoming</option>'
               f'</select>')

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    if error_text:
        for error in error_text:
            context += f'<div class="help-message text-danger">{error}</div>'

    context += f'</div>'

    return mark_safe(context)
