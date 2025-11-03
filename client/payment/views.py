from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import mail_managers
from django.http import Http404
from django.shortcuts import redirect
from django.template import loader
from django.views import generic

from client.payment import models
from util.merchant import authorizenet, eprocessing


class PaymentForm(forms.Form):
    """
    Client - Payment - Form
    """

    address = forms.CharField(required=True)

    city = forms.CharField(required=True)

    class_type = forms.CharField(required=True, widget=forms.HiddenInput)

    coupon_code = forms.CharField(required=False)

    credit_card_cvv2 = forms.CharField(required=True)

    credit_card_first_name = forms.CharField(required=True)

    credit_card_last_name = forms.CharField(required=True)

    credit_card_month = forms.CharField(required=True, widget=forms.Select)

    credit_card_number = forms.CharField(required=True)

    credit_card_year = forms.CharField(required=True, widget=forms.Select)

    email = forms.CharField(required=True)

    first_name = forms.CharField(required=True)

    ipaddress = forms.CharField(required=False)

    last_name = forms.CharField(required=True)

    policy = forms.BooleanField(required=True, widget=forms.CheckboxInput)

    phone = forms.CharField(required=True)

    state = forms.CharField(required=True, widget=forms.Select)

    suffix = forms.ChoiceField(required=False, widget=forms.Select, choices=models.Register.Suffix)

    zipcode = forms.CharField(required=True)

    def clean_coupon_code(self):
        coupon_code = self.cleaned_data['coupon_code']

        try:
            if coupon_code != '':
                models.Coupon.objects.get(name=coupon_code.upper(), class_type=self.cleaned_data['class_type'],
                                          is_active=True)
        except models.Coupon.DoesNotExist:
            raise ValidationError(
                f'Coupon Code is not valid. Please call or text us at {settings.PUBLIC_BUSINESS_PHONE} if you believe this is a valid coupon.',
                code='error')

        return coupon_code

    def charge(self):
        # Get Price Object
        try:
            result_price = models.Price.objects.get(class_type=self.cleaned_data['class_type'])
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        # Base Total Amount
        total_amount = result_price.amount

        # Coupon Code
        try:
            if self.cleaned_data['coupon_code'] != '':
                result_coupon = models.Coupon.objects.get(name=self.cleaned_data['coupon_code'].upper(),
                                                          class_type=self.cleaned_data['class_type'],
                                                          is_active=True)

                total_amount -= result_coupon.amount
        except models.Coupon.DoesNotExist:
            raise ValidationError(
                f'Coupon Code is not valid. Please call or text us at {settings.PUBLIC_BUSINESS_PHONE} if you believe this is a valid coupon.',
                code='error')

        # Total Cost
        self.cleaned_data['amount'] = total_amount

        # Charge Credit Card
        if result_price.is_active:
            # Authorize.Net Merchant
            if settings.MERCHANT_ID == 'authorizenet':
                payment = authorizenet.AuthorizeNet(self.cleaned_data).payment()
            # eProcessing Merchant
            elif settings.MERCHANT_ID == 'epn':
                payment = eprocessing.Eprocessing(self.cleaned_data).payment()
            else:
                # No available merchant
                raise ValidationError('No available merchant.', code='error')

            # Charge Declined
            if payment['error']:
                # Send Email
                self.send_email_declined(result_price, payment['message'])

                # Declined Error Message
                raise ValidationError(payment['message'], code='error')

            # Charge Successful
            else:
                # Send Email
                self.send_email_charged(result_price)

        # No Attempt to Charge Credit Card
        else:
            # Send Email
            self.send_email_charged(result_price)

    def send_email_declined(self, result: models.Price, payment=None):
        # Compose HTML Message
        html_message_fraud = loader.render_to_string(
            'client/payment/email/transaction_declined.html',
            {
                'address': self.cleaned_data['address'],
                'amount': result.amount,
                'city': self.cleaned_data['city'],
                'coupon_code': self.cleaned_data['coupon_code'] if self.cleaned_data.get('coupon_code') != '' else '',
                'credit_card_number': f"Name {self.cleaned_data['credit_card_first_name']} {self.cleaned_data['credit_card_last_name']} "
                                      f"# {self.cleaned_data['credit_card_number']} "
                                      f"EXP {self.cleaned_data['credit_card_month']} / {self.cleaned_data['credit_card_year']} "
                                      f"CVV {self.cleaned_data['credit_card_cvv2']}",
                'email': self.cleaned_data['email'],
                'first_name': self.cleaned_data['first_name'],
                'ipaddress': self.cleaned_data['ipaddress'],
                'last_name': self.cleaned_data['last_name'],
                'phone': self.cleaned_data['phone'],
                'reason': payment,
                'state': self.cleaned_data['state'],
                'suffix': self.cleaned_data['suffix'] if self.cleaned_data.get('suffix') is not None else '',
                'zipcode': self.cleaned_data['zipcode']
            }
        )

        # Email Managers
        mail_managers(
            subject=f"Declined Payment for {self.cleaned_data['first_name']} {self.cleaned_data['last_name']} - ${self.cleaned_data['amount']}",
            message=None,
            fail_silently=True,
            html_message=html_message_fraud
        )

    def send_email_charged(self, result: models.Price):
        if result.is_active:
            # Truncate Credit Card Details
            alter_credit_card_number = 'XXXX%s' % self.cleaned_data['credit_card_number'][-4:]
        else:
            # Do Not Truncate Credit Card Details
            alter_credit_card_number = f"Name {self.cleaned_data['credit_card_first_name']} {self.cleaned_data['credit_card_last_name']} " \
                                       f"# {self.cleaned_data['credit_card_number']} " \
                                       f"EXP {self.cleaned_data['credit_card_month']} / {self.cleaned_data['credit_card_year']} " \
                                       f"CVV {self.cleaned_data['credit_card_cvv2']}"

        # Compose HTML Message
        html_message = loader.render_to_string(
            'client/payment/email/payment.html',
            {
                'address': self.cleaned_data['address'],
                'amount': self.cleaned_data['amount'],
                'city': self.cleaned_data['city'],
                'coupon_code': self.cleaned_data['coupon_code'] if self.cleaned_data.get('coupon_code') != '' else '',
                'credit_card_number': alter_credit_card_number,
                'email': self.cleaned_data['email'],
                'first_name': self.cleaned_data['first_name'],
                'ipaddress': self.cleaned_data['ipaddress'],
                'last_name': self.cleaned_data['last_name'],
                'phone': self.cleaned_data['phone'],
                'state': self.cleaned_data['state'],
                'suffix': self.cleaned_data['suffix'] if self.cleaned_data.get('suffix') is not None else '',
                'zipcode': self.cleaned_data['zipcode']
            }
        )

        # Email Managers
        mail_managers(
            subject=f"Payment for {self.cleaned_data['first_name']} {self.cleaned_data['last_name']} - ${self.cleaned_data['amount']}",
            message=None,
            fail_silently=True,
            html_message=html_message
        )

        # If Coupon Code is one-time-use
        try:
            if self.cleaned_data['coupon_code'] != '':
                result_coupon = models.Coupon.objects.get(name=self.cleaned_data['coupon_code'].upper(),
                                                          class_type=self.cleaned_data['class_type'],
                                                          is_active=True)

                # Delete coupon
                if result_coupon.one_time_use:
                    result_coupon.delete()
        except models.Coupon.DoesNotExist:
            pass


class Index(generic.FormView):
    """
    Client - Payment - Index
    """

    form_class = PaymentForm
    template_name = 'client/payment/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Pay Online'
        context['keywords'] = 'payment, pay online'
        context['title'] = 'Pay Online'

        return context


class Payment(generic.FormView):
    """
    Client - Payment - Payment
    """

    form_class = PaymentForm
    template_name = 'client/payment/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Pay Online'
        context['keywords'] = 'payment, pay online'
        context['title'] = 'Pay Online'
        context['defaults'] = self.get_defaults()

        return context

    def get_defaults(self):
        try:
            result = models.Price.objects.get(class_type=self.kwargs['class_type'])
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        return {
            'amount': str(result.amount),
            'class_type': result.class_type,
            'process_amount': str(result.process_amount)
        }

    def form_valid(self, form):
        # Process Credit Card
        try:
            form.charge()
        except ValidationError as e:
            # There was a problem charging the credit card
            form.add_error(None, str(e))

            return self.form_invalid(form)

        return redirect('client-payment-confirmation', form.cleaned_data['class_type'])


class Confirmation(generic.TemplateView):
    """
    Client - Payment - Confirmation
    """

    template_name = 'client/payment/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Payment - Confirmation'
        context['keywords'] = ''
        context['title'] = 'Payment - Confirmation'
        context['process_amount'] = self.get_defaults()

        return context

    def get_defaults(self):
        try:
            result = models.Price.objects.get(class_type=self.kwargs['class_type'])
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        return result.process_amount
