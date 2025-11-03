from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import loader
from django.utils.decorators import method_decorator
from django.views import generic
from honeypot.decorators import check_honeypot


class ContactForm(forms.Form):
    """
    Client - Contact - Form
    """

    email = forms.CharField(required=False)

    contact = forms.CharField(required=True)

    ipaddress = forms.CharField(required=False)

    message = forms.CharField(required=True)

    name = forms.CharField(required=True)

    phone = forms.CharField(required=False)

    @staticmethod
    def send_email_check(cleaned_data: dict):
        # Contact Items
        blocked_contact = [
            'bestaitools.my',
            'monkeydigital.co',
        ]

        for blocked_item in blocked_contact:
            # Contact
            if blocked_item in cleaned_data['contact'].lower():
                return False

        # Message and Name Items
        blocked_items = [
            '.capital',
            '.com',
            '.net',
            '.org',
            '.expert',
            '@',
            '+',
            'companies',
            'competitor'
            'complimentary',
            'dashboard',
            'design',
            'developer',
            'fax',
            'gpt',
            'http',
            'https',
            'mailto',
            'merchant',
            'muh',
            'seo',
            'subscription'
            'technology',
            'unsubscribe',
            'video',
            'whatsapp',
            'www',
        ]

        for blocked_item in blocked_items:
            # Message
            if blocked_item in cleaned_data['message'].lower():
                return False

            # Name
            elif blocked_item in cleaned_data['name'].lower():
                return False

        if cleaned_data['email'] != '':
            return False
        else:
            return True

    def send_email(self, request):
        # Check if honeypot was used OR if an HTTP address was detected, if not, let's send the email
        if self.send_email_check(self.cleaned_data):
            # Compose HTML Message
            html_message = loader.render_to_string(
                'client/contact/email/contact.html',
                {
                    'email': self.cleaned_data['contact'],
                    'ipaddress': self.cleaned_data['ipaddress'],
                    'message': self.cleaned_data['message'],
                    'name': self.cleaned_data['name'],
                    'phone': self.cleaned_data['phone'] if self.cleaned_data['phone'] is not None else ''
                }
            )

            # Email Managers
            msg = EmailMessage(
                'New submission from Contact Us',
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
    Client - Contact - Index
    """

    form_class = ContactForm
    template_name = 'client/contact/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Contact Us'
        context['keywords'] = 'contact us, contact'
        context['title'] = 'Contact Us'

        return context

    def form_valid(self, form):
        # Send Email
        form.send_email(self.request)

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
