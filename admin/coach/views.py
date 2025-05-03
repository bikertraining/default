from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from admin.coach import models


class CoachForm(forms.Form):
    """
    Admin - Coach - Create / Update Form
    """

    address = forms.CharField(required=True)

    city = forms.CharField(required=True)

    date_to = forms.CharField(required=True)

    email = forms.CharField(required=True)

    frtp_date_from = forms.CharField(required=True)

    is_active = forms.BooleanField(required=False)

    msf_id = forms.CharField(required=False)

    name = forms.CharField(required=True)

    phone = forms.CharField(required=True)

    state = forms.CharField(required=True, widget=forms.Select())

    zipcode = forms.CharField(required=True)


class Index(LoginRequiredMixin, generic.ListView):
    """
    Admin - Coach - Index
    """

    template_name = 'admin/coach/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Search Coach'
        context['keywords'] = ''
        context['title'] = 'Search Coaches'

        return context

    def get_queryset(self):
        return models.Coach.objects.filter(is_active=True).order_by('name')


class Inactive(LoginRequiredMixin, generic.ListView):
    """
    Admin - Coach - Inactive
    """

    template_name = 'admin/coach/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Search Inactive Coach'
        context['keywords'] = ''
        context['title'] = 'Search Inactive Coaches'

        return context

    def get_queryset(self):
        return models.Coach.objects.filter(is_active=False).order_by('name')


class Create(LoginRequiredMixin, generic.FormView):
    """
    Admin - Coach - Create
    """

    form_class = CoachForm
    template_name = 'admin/coach/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Create Coach'
        context['keywords'] = ''
        context['title'] = 'Create Coach'

        return context

    def form_valid(self, form):
        # Create Coach
        models.Coach.objects.create(
            address=form.cleaned_data['address'],
            city=form.cleaned_data['city'],
            date_to=form.cleaned_data['date_to'],
            email=form.cleaned_data['email'],
            frtp_date_from=form.cleaned_data['frtp_date_from'],
            is_active=True,
            msf_id=form.cleaned_data['msf_id'],
            name=form.cleaned_data['name'],
            phone=form.cleaned_data['phone'],
            state=form.cleaned_data['state'],
            zipcode=form.cleaned_data['zipcode']
        )

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Coach has been created.')

        return redirect('admin-coach-index')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Edit(LoginRequiredMixin, FormMixin, generic.DetailView):
    """
    Admin - Coach - Edit
    """

    form_class = CoachForm
    template_name = 'admin/coach/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Edit Coach'
        context['keywords'] = ''
        context['title'] = 'Edit Coach'

        return context

    def get_object(self, queryset=None):
        try:
            return models.Coach.objects.get(id=self.kwargs['pk'])
        except models.Coach.DoesNotExist:
            raise Http404('Coach does not exist')

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Update Coach Object
        result = self.get_object()
        result.address = form.cleaned_data['address']
        result.city = form.cleaned_data['city']
        result.date_to = form.cleaned_data['date_to']
        result.email = form.cleaned_data['email']
        result.frtp_date_from = form.cleaned_data['frtp_date_from']
        result.is_active = form.cleaned_data['is_active']
        result.msf_id = form.cleaned_data['msf_id']
        result.name = form.cleaned_data['name']
        result.phone = form.cleaned_data['phone']
        result.state = form.cleaned_data['state']
        result.zipcode = form.cleaned_data['zipcode']
        result.save()

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Coach has been updated.')

        return redirect('admin-coach-index')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Delete(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    """
    Admin - Coach - Delete
    """

    model = models.Coach
    success_message = 'Coach has been deleted.'

    def get_success_url(self):
        return reverse('admin-coach-index')
