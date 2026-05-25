from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_form_select_dob_day(label, name, error_text=None, help_text=None, required=True, value=None):
    if error_text is None:
        error_text = {}

    context = (f'<div class="SelectInput{" required" if required else ""} mb-3">'
               f'<label class="fw-bold form-label" for={name}>{label}</label>'
               f'<select class="form-control{" is-invalid" if error_text else ""}" id="{name}" label="{label}" name="{name}">'
               f'<option value="">-- Select {label} --</option>'
               f'<option value="01"{" selected" if value == "01" else ""}>01</option>'
               f'<option value="02"{" selected" if value == "02" else ""}>02</option>'
               f'<option value="03"{" selected" if value == "03" else ""}>03</option>'
               f'<option value="04"{" selected" if value == "04" else ""}>04</option>'
               f'<option value="05"{" selected" if value == "05" else ""}>05</option>'
               f'<option value="06"{" selected" if value == "06" else ""}>06</option>'
               f'<option value="07"{" selected" if value == "07" else ""}>07</option>'
               f'<option value="08"{" selected" if value == "08" else ""}>08</option>'
               f'<option value="09"{" selected" if value == "09" else ""}>09</option>'
               f'<option value="10"{" selected" if value == "10" else ""}>10</option>'
               f'<option value="11"{" selected" if value == "11" else ""}>11</option>'
               f'<option value="12"{" selected" if value == "12" else ""}>12</option>'
               f'<option value="13"{" selected" if value == "13" else ""}>13</option>'
               f'<option value="14"{" selected" if value == "14" else ""}>14</option>'
               f'<option value="15"{" selected" if value == "15" else ""}>15</option>'
               f'<option value="16"{" selected" if value == "16" else ""}>16</option>'
               f'<option value="17"{" selected" if value == "17" else ""}>17</option>'
               f'<option value="18"{" selected" if value == "18" else ""}>18</option>'
               f'<option value="19"{" selected" if value == "19" else ""}>19</option>'
               f'<option value="20"{" selected" if value == "20" else ""}>20</option>'
               f'<option value="21"{" selected" if value == "21" else ""}>21</option>'
               f'<option value="22"{" selected" if value == "22" else ""}>22</option>'
               f'<option value="23"{" selected" if value == "23" else ""}>23</option>'
               f'<option value="24"{" selected" if value == "24" else ""}>24</option>'
               f'<option value="25"{" selected" if value == "25" else ""}>25</option>'
               f'<option value="26"{" selected" if value == "26" else ""}>26</option>'
               f'<option value="27"{" selected" if value == "27" else ""}>27</option>'
               f'<option value="28"{" selected" if value == "28" else ""}>28</option>'
               f'<option value="29"{" selected" if value == "29" else ""}>29</option>'
               f'<option value="30"{" selected" if value == "30" else ""}>30</option>'
               f'<option value="31"{" selected" if value == "31" else ""}>31</option>'
               f'</select>')

    if help_text is not None:
        context += f'<div class="form-text">{help_text}</div>'

    if error_text:
        for error in error_text:
            context += f'<div class="help-message text-danger">{error}</div>'

    context += f'</div>'

    return mark_safe(context)
