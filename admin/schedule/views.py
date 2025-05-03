from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from admin.schedule import models


class ScheduleForm(forms.Form):
    """
    Admin - Schedule - Create / Update Form
    """

    date_from = forms.CharField(required=True)

    date_to = forms.CharField(required=True)

    day_type = forms.ChoiceField(required=True, widget=forms.Select, choices=models.Schedule.DayType)

    price = forms.ChoiceField(required=True, widget=forms.Select, choices=models.Price.ClassType)

    seats = forms.CharField(required=True)


class Index(LoginRequiredMixin, generic.ListView):
    """
    Admin - Schedule - Index
    """

    template_name = 'admin/schedule/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Search Schedule'
        context['keywords'] = ''
        context['title'] = 'Search Schedule'

        return context

    def get_queryset(self):
        return models.Schedule.objects.all().order_by('date_from')


class Create(LoginRequiredMixin, generic.FormView):
    """
    Admin - Schedule - Create
    """

    form_class = ScheduleForm
    template_name = 'admin/schedule/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Create Schedule'
        context['keywords'] = ''
        context['title'] = 'Create Schedule'

        return context

    def form_valid(self, form):
        # Get Price Object
        try:
            result = models.Price.objects.get(class_type=form.cleaned_data['price'])
        except models.Price.DoesNotExist:
            raise Http404('Price does not exist')

        # Create Schedule
        models.Schedule.objects.create(
            date_from=form.cleaned_data['date_from'],
            date_to=form.cleaned_data['date_to'],
            day_type=form.cleaned_data['day_type'],
            price=result,
            seats=form.cleaned_data['seats']
        )

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Schedule has been created.')

        return redirect('admin-schedule-index')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Edit(LoginRequiredMixin, FormMixin, generic.DetailView):
    """
    Admin - Schedule - Edit
    """

    form_class = ScheduleForm
    template_name = 'admin/schedule/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Edit Schedule'
        context['keywords'] = ''
        context['title'] = 'Edit Schedule'
        context['students'] = self.get_students()

        return context

    def get_object(self, queryset=None):
        try:
            return models.Schedule.objects.get(id=self.kwargs['pk'])
        except models.Schedule.DoesNotExist:
            raise Http404('Schedule does not exist')

    def get_students(self):
        return models.Register.objects.filter(schedule=self.get_object())

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Get Price Object
        try:
            result_price = models.Price.objects.get(class_type=form.cleaned_data['price'])
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        # Update Schedule Object
        result = self.get_object()
        result.date_from = form.cleaned_data['date_from']
        result.date_to = form.cleaned_data['date_to']
        result.day_type = form.cleaned_data['day_type']
        result.price = result_price
        result.seats = form.cleaned_data['seats']
        result.save()

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Schedule has been updated.')

        return redirect('admin-schedule-index')

    def form_invalid(self, form):
        return super().form_invalid(form)


class Delete(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    """
    Admin - Schedule - Delete
    """

    model = models.Schedule
    success_message = 'Schedule has been deleted.'

    def get_success_url(self):
        return reverse('admin-schedule-index')


class Print(generic.TemplateView):
    """
    Admin - Schedule - print
    """

    template_name = 'admin/schedule/print.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Print Student Registration'
        context['keywords'] = ''
        context['title'] = 'Print Student Registration'
        context['registration'] = self.get_registration()

        return context

    def get_registration(self):
        try:
            return models.Register.objects.get(schedule=self.kwargs['pk'], pk=self.kwargs['student_pk'])
        except models.Register.DoesNotExist:
            raise Http404('Registration does not exist')
