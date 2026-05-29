from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import loader
from django.views import generic

from client.contact import models


class ContactForm(forms.Form):
    """
    Client - Contact - Form
    """

    email = forms.EmailField(required=True)

    ipaddress = forms.CharField(required=False)

    message = forms.CharField(required=True)

    name = forms.CharField(required=True)

    phone = forms.CharField(required=False)

    def send_email(self):
        # Compose HTML Message
        html_message = loader.render_to_string(
            'client/contact/email/contact.html',
            {
                'email': self.cleaned_data['email'],
                'ipaddress': self.cleaned_data['ipaddress'],
                'message': self.cleaned_data['message'],
                'name': self.cleaned_data['name'],
                'phone': self.cleaned_data['phone'] if self.cleaned_data['phone'] is not None else ''
            }
        )

        # Email Managers
        try:
            msg = EmailMessage(
                'New submission from Contact Us',
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
    Client - Contact - Index
    """

    form_class = ContactForm
    template_name = 'client/contact/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = ('Have questions about motorcycle training, scheduling, or licensing? '
                                  'Contact Biker Training LLC for support, enrollment help, and general inquiries.')
        context['keywords'] = ('contact biker training, motorcycle training contact, rider course support, '
                               'motorcycle class help, training questions')
        context['title'] = 'Contact Biker Training LLC | Get in Touch'

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

            # Message
            if item.name.lower() in form.cleaned_data['message'].lower():
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
            return redirect('client-contact-blocked')

        # Send Email
        form.send_email()

        # Redirect
        return redirect('client-contact-confirmation')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Confirmation(generic.TemplateView):
    """
    Client - Contact - Confirmation
    """

    template_name = 'client/contact/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Contact Us - Confirmation'
        context['keywords'] = ''
        context['title'] = 'Contact Us - Confirmation'

        return context


class Blocked(generic.TemplateView):
    """
    Client - Contact - Blocked
    """

    template_name = 'client/contact/blocked.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Contact Us - Blocked'
        context['keywords'] = ''
        context['title'] = 'Contact Us - Blocked'

        return context
