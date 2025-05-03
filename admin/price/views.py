from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import FormMixin

from admin.price import models


class PriceForm(forms.Form):
    """
    Admin - Price - Update Form
    """

    amount = forms.CharField(required=True)

    is_active = forms.BooleanField(required=False)

    process_amount = forms.CharField(required=True)

    re_amount = forms.CharField(required=True)


class Index(LoginRequiredMixin, generic.ListView):
    """
    Admin - Price - Index
    """

    template_name = 'admin/price/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Search Prices'
        context['keywords'] = ''
        context['title'] = 'Search Prices'

        return context

    def get_queryset(self):
        return models.Price.objects.all()


class Edit(LoginRequiredMixin, FormMixin, generic.DetailView):
    """
    Admin - Price - Edit
    """

    form_class = PriceForm
    template_name = 'admin/price/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Edit Price'
        context['keywords'] = ''
        context['title'] = 'Edit Price'

        return context

    def get_object(self, queryset=None):
        try:
            return models.Price.objects.get(id=self.kwargs['pk'])
        except models.Price.DoesNotExist:
            raise Http404('Price does not exist')

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Update Price Object
        result = self.get_object()
        result.amount = form.cleaned_data['amount']
        result.re_amount = form.cleaned_data['re_amount']
        result.process_amount = form.cleaned_data['process_amount']
        result.is_active = form.cleaned_data['is_active']
        result.save()

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Price has been updated.')

        return redirect('admin-price-index')

    def form_invalid(self, form):
        return super().form_invalid(form)
