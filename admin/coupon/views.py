from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from admin.coupon import models


class CouponForm(forms.Form):
    """
    Admin - Coupon - Create / Update Form
    """

    amount = forms.CharField(required=True)

    class_type = forms.ChoiceField(required=True, widget=forms.Select, choices=models.Price.ClassType)

    is_active = forms.BooleanField(required=False)

    name = forms.CharField(required=True)

    one_time_use = forms.BooleanField(required=False)


class Index(LoginRequiredMixin, generic.ListView):
    """
    Admin - Coupon - Index
    """

    template_name = 'admin/coupon/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Search Coupons'
        context['keywords'] = ''
        context['title'] = 'Search Coupons'

        return context

    def get_queryset(self):
        return models.Coupon.objects.all().order_by('name')


class Create(LoginRequiredMixin, generic.FormView):
    """
    Admin - Coupon - Create
    """

    form_class = CouponForm
    template_name = 'admin/coupon/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Create Coupon'
        context['keywords'] = ''
        context['title'] = 'Create Coupon'

        return context

    def form_valid(self, form):
        # Create Schedule
        models.Coupon.objects.create(
            amount=form.cleaned_data['amount'],
            class_type=form.cleaned_data['class_type'],
            is_active=form.cleaned_data['is_active'],
            name=form.cleaned_data['name'].upper(),
            one_time_use=form.cleaned_data['one_time_use']
        )

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Coupon has been created.')

        return redirect('admin-coupon-index')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Edit(LoginRequiredMixin, FormMixin, generic.DetailView):
    """
    Admin - Coupon - Edit
    """

    form_class = CouponForm
    template_name = 'admin/coupon/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Edit Coupon'
        context['keywords'] = ''
        context['title'] = 'Edit Coupon'

        return context

    def get_object(self, queryset=None):
        try:
            return models.Coupon.objects.get(id=self.kwargs['pk'])
        except models.Coupon.DoesNotExist:
            raise Http404('Coupon does not exist')

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Update Coupon Object
        result = self.get_object()
        result.amount = form.cleaned_data['amount']
        result.class_type = form.cleaned_data['class_type']
        result.is_active = form.cleaned_data['is_active']
        result.name = form.cleaned_data['name'].upper()
        result.one_time_use = form.cleaned_data['one_time_use']
        result.save()

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Coupon has been updated.')

        return redirect('admin-coupon-index')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Delete(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    """
    Admin - Coupon - Delete
    """

    model = models.Coupon
    success_message = 'Coupon has been deleted.'

    def get_success_url(self):
        return reverse('admin-coupon-index')
