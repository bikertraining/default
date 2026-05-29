from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views import generic

from admin.fraud import models


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


class Create(LoginRequiredMixin, generic.CreateView):
    """
    Admin - Fraud - Create
    """

    model = models.Fraud
    fields = ['fraud_type', 'name']
    template_name = 'admin/fraud/create.html'
    success_url = reverse_lazy('admin-fraud-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Create Fraud String'
        context['keywords'] = ''
        context['title'] = 'Create Fraud String'

        return context

    def form_valid(self, form):
        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Fraud string has been created.')

        return super(Create, self).form_valid(form)


class Edit(LoginRequiredMixin, generic.UpdateView):
    """
    Admin - Fraud - Edit
    """

    model = models.Fraud
    fields = ['fraud_type', 'is_active']
    template_name = 'admin/fraud/edit.html'
    success_url = reverse_lazy('admin-fraud-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Edit Fraud String'
        context['keywords'] = ''
        context['title'] = 'Edit Fraud String'

        return context

    def form_valid(self, form):
        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Fraud string has been updated.')

        return super(Edit, self).form_valid(form)


class Delete(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    """
    Admin - Fraud - Delete
    """

    model = models.Fraud
    success_message = 'Fraud string has been deleted.'

    def get_success_url(self):
        return reverse('admin-fraud-index')
