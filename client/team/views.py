from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import loader
from django.views import generic
from turnstile.fields import TurnstileField

from client.team import models


class TeamForm(forms.Form):
    """
    Client - Team - Form
    """

    email = forms.CharField(required=True)

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

    turnstile = TurnstileField()

    def send_email(self):
        # Compose HTML Message
        html_message = loader.render_to_string(
            'client/team/email/join.html',
            {
                'email': self.cleaned_data['email'],
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
        try:
            msg = EmailMessage(
                'New submission from Join Our Team',
                html_message,
                settings.DEFAULT_FROM_EMAIL,
                settings.MANAGERS,
                reply_to=[self.cleaned_data['email']]
            )
            msg.content_subtype = 'html'
            msg.send()
        except Exception:
            pass


class Index(generic.FormView):
    """
    Client - Team - Index
    """

    form_class = TeamForm
    template_name = 'client/team/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            'description'] = 'Learn about their experience, credentials, and dedication to rider safety and education.'
        context[
            'keywords'] = 'motorcycle instructors, rider training team, motorcycle safety instructors, rider education staff'
        context['title'] = 'Join our Team'

        return context

    @staticmethod
    def detect_fraud(form):
        # IP Address
        if models.Fraud.objects.filter(fraud_type='ipaddress', is_active=True,
                                       name=form.cleaned_data['ipaddress']).exists():
            return True

        elif form.cleaned_data['ipaddress'] is None or form.cleaned_data['ipaddress'] == '' or form.cleaned_data[
            'ipaddress'] == 'None':
            return True

        # Email / General
        for item in models.Fraud.objects.filter(fraud_type__in=['email', 'general'], is_active=True):
            # Email Address
            if item.name.lower() in form.cleaned_data['email'].lower():
                return True

            # Message 1
            if item.name.lower() in form.cleaned_data['message1'].lower():
                return True

            # Message 2
            elif item.name.lower() in form.cleaned_data['message2'].lower():
                return True

            # Message 3
            elif item.name.lower() in form.cleaned_data['message3'].lower():
                return True

            # Message 4
            elif item.name.lower() in form.cleaned_data['message4'].lower():
                return True

            # Message 5
            elif item.name.lower() in form.cleaned_data['message5'].lower():
                return True

            # Message 6
            elif item.name.lower() in form.cleaned_data['message6'].lower():
                return True

            # Message 7
            elif item.name.lower() in form.cleaned_data['message7'].lower():
                return True

            # Name
            elif item.name.lower() in form.cleaned_data['name'].lower():
                return True

        # Success - Nothing bad detected
        else:
            return False

    def form_valid(self, form):
        # Detect Fraud
        if self.detect_fraud(form):
            return redirect('client-team-blocked')

        # Send Email
        form.send_email()

        # Redirect
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


class Blocked(generic.TemplateView):
    """
    Client - Team - Blocked
    """

    template_name = 'client/team/blocked.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Join our Team - Blocked'
        context['keywords'] = ''
        context['title'] = 'Join our Team - Blocked'

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
        context['title'] = 'RiderCoach Freqently Asked Questions'

        return context
