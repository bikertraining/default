from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from admin.fraud import models


class FraudForm(forms.Form):
    """
    Admin - Fraud - Create / Update Form
    """

    fraud_type = forms.ChoiceField(required=True, widget=forms.Select, choices=models.Fraud.FraudType)

    is_active = forms.BooleanField(required=False)

    name = forms.CharField(required=True)


class Index(LoginRequiredMixin, generic.ListView):
    """
    Admin - Fraud - Index
    """

    template_name = 'admin/fraud/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Search Fraud Strings'
        context['keywords'] = ''
        context['title'] = 'Search Fraud Strings'

        return context

    def get_queryset(self):
        return models.Fraud.objects.filter().order_by('fraud_type')


class Create(LoginRequiredMixin, generic.FormView):
    """
    Admin - Fraud - Create
    """

    form_class = FraudForm
    template_name = 'admin/fraud/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Create Fraud String'
        context['keywords'] = ''
        context['title'] = 'Create Fraud String'

        return context

    def form_valid(self, form):
        # Sanitize
        if form.cleaned_data['fraud_type'] == 'email' or form.cleaned_data['fraud_type'] == 'general':
            name = form.cleaned_data['name'].lower()
        else:
            name = form.cleaned_data['name']

        # Create Fraud
        models.Fraud.objects.create(
            fraud_type=form.cleaned_data['fraud_type'],
            name=name
        )

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Fraud string has been created.')

        return redirect('admin-fraud-index')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Edit(LoginRequiredMixin, FormMixin, generic.DetailView):
    """
    Admin - Fraud - Edit
    """

    form_class = FraudForm
    template_name = 'admin/fraud/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Edit Fraud String'
        context['keywords'] = ''
        context['title'] = 'Edit Fraud String'

        return context

    def get_object(self, queryset=None):
        try:
            return models.Fraud.objects.get(id=self.kwargs['pk'])
        except models.Fraud.DoesNotExist:
            raise Http404('Fraud string does not exist')

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Sanitize
        if form.cleaned_data['fraud_type'] == 'email' or form.cleaned_data['fraud_type'] == 'general':
            name = form.cleaned_data['name'].lower()
        else:
            name = form.cleaned_data['name']

        # Update Fraud Object
        result = self.get_object()
        result.fraud_type = form.cleaned_data['fraud_type']
        result.is_active = form.cleaned_data['is_active']
        result.name = name
        result.save()

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Fraud string has been updated.')

        return redirect('admin-fraud-index')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Delete(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    """
    Admin - Fraud - Delete
    """

    model = models.Fraud
    success_message = 'Fraud string has been deleted.'

    def get_success_url(self):
        return reverse('admin-fraud-index')
