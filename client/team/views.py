from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import generic
from honeypot.decorators import check_honeypot


class TeamForm(forms.Form):
    """
    Client - Team - Form
    """

    email = forms.CharField(required=False)

    contact = forms.CharField(required=True)

    ipaddress = forms.CharField(required=False)

    message1 = forms.CharField(required=True)

    message2 = forms.CharField(required=True)

    message3 = forms.CharField(required=True)

    message4 = forms.CharField(required=True)

    message5 = forms.CharField(required=True)

    message6 = forms.CharField(required=True)

    message7 = forms.CharField(required=True)

    name = forms.CharField(required=True)

    phone = forms.CharField(required=True)

    @staticmethod
    def send_email_check(email='', message1='', message2='', message3='', message4='', message5='', message6='',
                         message7=''):
        if 'http' in message1 or 'https' in message1 or 'mailto' in message1 or '@' in message1:
            return False
        elif 'http' in message2 or 'https' in message2 or 'mailto' in message2 or '@' in message2:
            return False
        elif 'http' in message3 or 'https' in message3 or 'mailto' in message3 or '@' in message3:
            return False
        elif 'http' in message4 or 'https' in message4 or 'mailto' in message4 or '@' in message4:
            return False
        elif 'http' in message5 or 'https' in message5 or 'mailto' in message5 or '@' in message5:
            return False
        elif 'http' in message6 or 'https' in message6 or 'mailto' in message6 or '@' in message6:
            return False
        elif 'http' in message7 or 'https' in message7 or 'mailto' in message7 or '@' in message7:
            return False
        elif email != '':
            return False
        else:
            return True

    def send_email(self):
        # Check if honeypot was used OR if an HTTP address was detected, if not, let's send the email
        if self.send_email_check(self.cleaned_data['email'], self.cleaned_data['message1'],
                                 self.cleaned_data['message2'], self.cleaned_data['message3'],
                                 self.cleaned_data['message4'], self.cleaned_data['message5'],
                                 self.cleaned_data['message6'], self.cleaned_data['message7']):
            # Compose HTML Message
            html_message = loader.render_to_string(
                'client/team/email/join.html',
                {
                    'email': self.cleaned_data['contact'],
                    'ipaddress': self.cleaned_data['ipaddress'],
                    'message1': self.cleaned_data['message1'],
                    'message2': self.cleaned_data['message2'],
                    'message3': self.cleaned_data['message3'],
                    'message4': self.cleaned_data['message4'],
                    'message5': self.cleaned_data['message5'],
                    'message6': self.cleaned_data['message6'],
                    'message7': self.cleaned_data['message7'],
                    'name': self.cleaned_data['name'],
                    'phone': self.cleaned_data['phone']
                }
            )

            # Email Managers
            msg = EmailMessage(
                'New submission from Join Our Team',
                html_message,
                settings.DEFAULT_FROM_EMAIL,
                settings.MANAGERS,
                reply_to=[self.cleaned_data['contact']]
            )
            msg.content_subtype = 'html'
            msg.send()


@method_decorator(check_honeypot, name='post')
class Index(generic.FormView):
    """
    Client - Team - Index
    """

    form_class = TeamForm
    template_name = 'client/team/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Become a RiderCoach'
        context['keywords'] = 'rider coach, ridercoach, coach, teach, teacher, instructor'
        context['title'] = 'Join our Team'

        return context

    def form_valid(self, form):
        # Send Email
        form.send_email()

        return redirect('client-team-confirmation')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Confirmation(generic.TemplateView):
    """
    Client - Team - Confirmation
    """

    template_name = 'client/team/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Join our Team - Confirmation'
        context['keywords'] = ''
        context['title'] = 'Join our Team - Confirmation'

        return context


class Faq(generic.TemplateView):
    """
    Client - Team - FAQ
    """

    template_name = 'client/team/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'RiderCoach Frequently Asked Questions'
        context['keywords'] = 'ridercoach frequently asked questions, ridercoach, rider coach, coach, instructor, faq'
        context['title'] = 'RiderCoach FAQ'

        return context
