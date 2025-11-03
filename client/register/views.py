from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import mail_managers
from django.http import Http404
from django.shortcuts import redirect
from django.template import loader
from django.views import generic

from client.register import models
from util.merchant import authorizenet, eprocessing, filters


class RegisterForm(forms.Form):
    """
    Client - Register - Form
    """

    address = forms.CharField(required=True)

    city = forms.CharField(required=True)

    class_type = forms.CharField(required=True, widget=forms.HiddenInput)

    comment = forms.CharField(required=False)

    coupon_code = forms.CharField(required=False)

    credit_card_cvv2 = forms.CharField(required=True)

    credit_card_first_name = forms.CharField(required=True)

    credit_card_last_name = forms.CharField(required=True)

    credit_card_month = forms.CharField(required=True, widget=forms.Select)

    credit_card_number = forms.CharField(required=True)

    credit_card_year = forms.CharField(required=True, widget=forms.Select)

    dln = forms.CharField(required=True)

    dls = forms.CharField(required=True, widget=forms.Select)

    dob = forms.CharField(required=True)

    email = forms.CharField(required=True)

    first_name = forms.CharField(required=True)

    ipaddress = forms.CharField(required=False)

    last_name = forms.CharField(required=True)

    phone = forms.CharField(required=True)

    policy = forms.BooleanField(required=True, widget=forms.CheckboxInput)

    schedule = forms.CharField(required=True, widget=forms.HiddenInput)

    state = forms.CharField(required=True, widget=forms.Select)

    suffix = forms.ChoiceField(required=False, widget=forms.Select, choices=models.Register.Suffix)

    xpl = forms.CharField(required=False, widget=forms.Select())

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
        # Get Schedule Object
        try:
            result_schedule = models.Schedule.objects.get(pk=self.cleaned_data['schedule'])
        except models.Schedule.DoesNotExist:
            raise Http404('Schedule does not exist')

        # Description
        self.cleaned_data['description'] = (
            f'{result_schedule.price.get_class_type_display()} - {result_schedule.get_day_type_display()} '
            f'/ {result_schedule.date_from} - {result_schedule.date_to}')

        # Base Total Amount
        total_amount = result_schedule.price.amount

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
        if result_schedule.price.is_active:
            # Authorize.Net Merchant
            if settings.MERCHANT_ID == 'authorizenet':
                payment = authorizenet.AuthorizeNet(self.cleaned_data).charge()
            # eProcessing Merchant
            elif settings.MERCHANT_ID == 'epn':
                payment = eprocessing.Eprocessing(self.cleaned_data).charge()
            else:
                # No available merchant
                raise ValidationError('No available merchant.', code='error')

            # Charge Declined
            if payment['error']:
                # Send Email
                self.send_email_declined(result_schedule, payment['message'])

                # Declined Error Message
                raise ValidationError(payment['message'], code='error')

            # Charge Successful
            else:
                # Send Email
                self.send_email_charged(result_schedule)

        # No Attempt to Charge Credit Card
        else:
            # Send Email
            self.send_email_charged(result_schedule)

    def send_email_declined(self, result: models.Schedule, payment=None):
        # Compose HTML Message
        html_message_fraud = loader.render_to_string(
            'client/register/email/transaction_declined.html',
            {
                'address': self.cleaned_data['address'],
                'city': self.cleaned_data['city'],
                'amount': self.cleaned_data['amount'],
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

    def send_email_charged(self, result: models.Schedule):
        # Subtract seat from schedule
        result.seats = int(result.seats) - 1
        result.save(update_fields=['seats'])

        if result.price.is_active:
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
            'client/register/email/register.html',
            {
                'address': self.cleaned_data['address'],
                'amount': self.cleaned_data['amount'],
                'city': self.cleaned_data['city'],
                'class_type': result.price.get_class_type_display(),
                'comment': self.cleaned_data['comment'] if self.cleaned_data.get('comment') is not None else '',
                'coupon_code': self.cleaned_data['coupon_code'] if self.cleaned_data.get('coupon_code') != '' else '',
                'credit_card_number': alter_credit_card_number,
                'dln': self.cleaned_data['dln'],
                'dls': self.cleaned_data['dls'],
                'dob': self.cleaned_data['dob'],
                'email': self.cleaned_data['email'],
                'first_name': self.cleaned_data['first_name'],
                'ipaddress': self.cleaned_data['ipaddress'],
                'last_name': self.cleaned_data['last_name'],
                'phone': self.cleaned_data['phone'],
                'schedule': filters.format_date(str(result.date_from),
                                                str(result.date_to)),
                'schedule_day': result.get_day_type_display(),
                'state': self.cleaned_data['state'],
                'suffix': self.cleaned_data['suffix'] if self.cleaned_data.get('suffix') is not None else '',
                'xpl': filters.format_xpl(
                    self.cleaned_data['xpl'] if self.cleaned_data.get('xpl') is not None else 'none'),
                'zipcode': self.cleaned_data['zipcode']
            }
        )

        # Email Managers
        mail_managers(
            subject=f"Course Registration for {result.price.get_class_type_display()} - ${self.cleaned_data['amount']}",
            message=None,
            fail_silently=True,
            html_message=html_message
        )

        # Save Student Information - Will be removed once class is deleted
        # This is only here in case an email was not received, and we are missing information
        models.Register.objects.create(
            address=self.cleaned_data['address'],
            amount=self.cleaned_data['amount'],
            city=self.cleaned_data['city'],
            class_type=result.price.get_class_type_display(),
            comment=self.cleaned_data['comment'] if self.cleaned_data.get('comment') is not None else '',
            coupon_code=self.cleaned_data['coupon_code'] if self.cleaned_data.get('coupon_code') != '' else '',
            credit_card_number=alter_credit_card_number,
            dln=self.cleaned_data['dln'],
            dls=self.cleaned_data['dls'],
            dob=self.cleaned_data['dob'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            schedule_date=filters.format_date(str(result.date_from),
                                              str(result.date_to)),
            schedule_day=result.get_day_type_display(),
            state=self.cleaned_data['state'],
            suffix=self.cleaned_data['suffix'] if self.cleaned_data.get('suffix') is not None else '',
            xpl=filters.format_xpl(self.cleaned_data['xpl'] if self.cleaned_data.get('xpl') is not None else 'none'),
            zipcode=self.cleaned_data['zipcode'],
            schedule=result
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
    Client - Register - Index
    """

    form_class = RegisterForm
    template_name = 'client/register/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Register Online'
        context['keywords'] = 'register online, register'
        context['title'] = 'Register Online'
        context['defaults'] = self.get_defaults()

        return context

    def get_defaults(self):
        try:
            result = models.Schedule.objects.get(id=self.kwargs['id'])
        except models.Schedule.DoesNotExist:
            raise Http404('Schedule does not exist')

        return {
            'amount': str(result.price.amount),
            'class_type': result.price.class_type,
            'date_from': result.date_from,
            'date_to': result.date_to,
            'day_type': result.day_type,
            'get_day_type_display': result.get_day_type_display(),
            'get_class_type_display': result.price.get_class_type_display(),
            'process_amount': str(result.price.process_amount),
            'schedule': result.id
        }

    @staticmethod
    def send_email_waitlist(form: RegisterForm, result: models.Schedule):
        # Compose HTML Message
        html_message = loader.render_to_string(
            'client/register/email/wait_list.html',
            {
                'address': form.cleaned_data['address'],
                'amount': result.price.amount,
                'city': form.cleaned_data['city'],
                'class_type': result.price.get_class_type_display(),
                'comment': form.cleaned_data['comment'] if form.cleaned_data.get('comment') is not None else '',
                'coupon_code': form.cleaned_data['coupon_code'] if form.cleaned_data.get('coupon_code') != '' else '',
                'dln': form.cleaned_data['dln'],
                'dls': form.cleaned_data['dls'],
                'dob': form.cleaned_data['dob'],
                'email': form.cleaned_data['email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'phone': form.cleaned_data['phone'],
                'schedule': filters.format_date(str(result.date_from),
                                                str(result.date_to)),
                'schedule_day': result.get_day_type_display(),
                'state': form.cleaned_data['state'],
                'suffix': form.cleaned_data['suffix'] if form.cleaned_data.get('suffix') is not None else '',
                'xpl': filters.format_xpl(
                    form.cleaned_data['xpl'] if form.cleaned_data.get('xpl') is not None else 'none'),
                'zipcode': form.cleaned_data['zipcode']
            }
        )

        # Email Managers
        mail_managers(
            subject=f"Wait List for {result.price.get_class_type_display()} - ${result.price.amount}",
            message=None,
            fail_silently=True,
            html_message=html_message
        )

    def form_valid(self, form):
        try:
            result = models.Schedule.objects.get(id=self.kwargs['id'])
        except models.Schedule.DoesNotExist:
            raise Http404('Schedule does not exist')

        # Validate we actually have enough seats
        if result.seats <= '0':
            # Send Wait List Email
            self.send_email_waitlist(form, result)

            return redirect('client-register-class-full')

        # Process Credit Card
        try:
            form.charge()
        except ValidationError as e:
            # There was a problem charging the credit card
            form.add_error(None, str(e))

            return self.form_invalid(form)

        return redirect('client-register-confirmation', form.cleaned_data['class_type'])

    def form_invalid(self, form):
        return super().form_invalid(form)


class Confirmation(generic.TemplateView):
    """
    Client - Register - Confirmation
    """

    template_name = 'client/register/confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Register - Confirmation'
        context['keywords'] = ''
        context['title'] = 'Register - Confirmation'
        context['process_amount'] = self.get_defaults()

        return context

    def get_defaults(self):
        try:
            result = models.Price.objects.get(class_type=self.kwargs['class_type'])
        except models.Price.DoesNotExist:
            raise Http404('Price does not exist')

        return result.process_amount


class ClassFull(generic.TemplateView):
    """
    Client - Register - Class Full
    """

    template_name = 'client/register/class_full.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Register - Class Full'
        context['keywords'] = ''
        context['title'] = 'Register - Class Full'

        return context
