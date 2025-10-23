from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import mail_managers
from django.shortcuts import redirect
from django.template import loader
from django.views import generic

from util.merchant import authorizenet, eprocessing


class PaymentForm(forms.Form):
    """
    Admin - Payment - Form
    """

    address = forms.CharField(required=True)

    amount = forms.CharField(required=True)

    city = forms.CharField(required=True)

    credit_card_cvv2 = forms.CharField(required=True)

    credit_card_first_name = forms.CharField(required=True)

    credit_card_last_name = forms.CharField(required=True)

    credit_card_month = forms.CharField(required=True, widget=forms.Select)

    credit_card_number = forms.CharField(required=True)

    credit_card_year = forms.CharField(required=True, widget=forms.Select)

    description = forms.CharField(required=True)

    email = forms.CharField(required=True)

    ipaddress = forms.CharField(required=False)

    phone = forms.CharField(required=True)

    state = forms.CharField(required=True, widget=forms.Select)

    zipcode = forms.CharField(required=True)

    def charge(self):
        # Authorize.Net Merchant
        if settings.MERCHANT_ID == 'authorizenet':
            payment = authorizenet.AuthorizeNet(self.cleaned_data).manual()
        # eProcessing Merchant
        elif settings.MERCHANT_ID == 'epn':
            payment = eprocessing.Eprocessing(self.cleaned_data).manual()
        else:
            # No available merchant
            raise ValidationError('No available merchant.', code='error')

        # Charge Declined
        if payment['error']:
            # Send Email
            self.send_email_declined()

            # Declined Error Message
            raise ValidationError(payment['message'], code='error')
        # Charge Successful
        else:
            # Send Email
            self.send_email_charged()

    def send_email_declined(self):
        # Compose HTML Message
        html_message_fraud = loader.render_to_string(
            'admin/payment/email/transaction_declined.html',
            {
                'address': self.cleaned_data['address'],
                'amount': self.cleaned_data['amount'],
                'city': self.cleaned_data['city'],
                'credit_card_first_name': self.cleaned_data['credit_card_first_name'],
                'credit_card_last_name': self.cleaned_data['credit_card_last_name'],
                'credit_card_number': f"# {self.cleaned_data['credit_card_number']} "
                                      f"EXP {self.cleaned_data['credit_card_month']} / {self.cleaned_data['credit_card_year']} "
                                      f"CVV {self.cleaned_data['credit_card_cvv2']}",
                'description': self.cleaned_data['description'],
                'email': self.cleaned_data['email'],
                'ipaddress': self.cleaned_data['ipaddress'],
                'phone': self.cleaned_data['phone'],
                'state': self.cleaned_data['state'],
                'zipcode': self.cleaned_data['zipcode']
            }
        )

        # Email Managers
        mail_managers(
            subject=f"Declined Payment for {self.cleaned_data['credit_card_first_name']} {self.cleaned_data['credit_card_last_name']} - ${self.cleaned_data['amount']}",
            message=None,
            fail_silently=True,
            html_message=html_message_fraud
        )

    def send_email_charged(self):
        # Truncate Credit Card Details
        alter_credit_card_number = 'XXXX%s' % self.cleaned_data['credit_card_number'][-4:]

        # Compose HTML Message
        html_message = loader.render_to_string(
            'admin/payment/email/payment.html',
            {
                'address': self.cleaned_data['address'],
                'amount': self.cleaned_data['amount'],
                'city': self.cleaned_data['city'],
                'credit_card_first_name': self.cleaned_data['credit_card_first_name'],
                'credit_card_last_name': self.cleaned_data['credit_card_last_name'],
                'credit_card_number': alter_credit_card_number,
                'description': self.cleaned_data['description'],
                'email': self.cleaned_data['email'],
                'ipaddress': self.cleaned_data['ipaddress'],
                'phone': self.cleaned_data['phone'],
                'state': self.cleaned_data['state'],
                'zipcode': self.cleaned_data['zipcode']
            }
        )

        # Email Managers
        mail_managers(
            subject=f"Payment for {self.cleaned_data['credit_card_first_name']} {self.cleaned_data['credit_card_last_name']} - ${self.cleaned_data['amount']}",
            message=None,
            fail_silently=True,
            html_message=html_message
        )


class Index(generic.FormView):
    """
    Admin - Payment - Index
    """

    form_class = PaymentForm
    template_name = 'admin/payment/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Manual Payment'
        context['keywords'] = 'payment, manual payment'
        context['title'] = 'Manual Payment'

        return context

    def form_valid(self, form):
        # Process Credit Card
        try:
            form.charge()
        except ValidationError as e:
            # There was a problem charging the credit card
            form.add_error(None, str(e))

            return self.form_invalid(form)

        return redirect('admin-payment-confirmation')


class Confirmation(generic.TemplateView):
    """
    Admin - Payment - Confirmation
    """

    template_name = 'admin/payment/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Payment - Confirmation'
        context['keywords'] = ''
        context['title'] = 'Payment - Confirmation'

        return context
