from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import FormMixin

from admin.ecourse import models


class EcourseForm(forms.Form):
    """
    Admin - eCourse - Create / Update Form
    """

    link_3wbrc = forms.CharField(required=True)

    link_brc = forms.CharField(required=True)

    link_src = forms.CharField(required=True)


class Index(LoginRequiredMixin, FormMixin, generic.DetailView):
    """
    Admin - eCourse - Index
    """

    form_class = EcourseForm
    template_name = 'admin/ecourse/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'eCourse Links'
        context['keywords'] = ''
        context['title'] = 'eCourse Links'

        return context

    def get_object(self, queryset=None):
        try:
            return models.Ecourse.objects.get(id=1)
        except models.Ecourse.DoesNotExist:
            raise Http404('eCourse does not exist')

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Update eCourse Object
        result = self.get_object()
        result.link_3wbrc = form.cleaned_data['link_3wbrc']
        result.link_brc = form.cleaned_data['link_brc']
        result.link_src = form.cleaned_data['link_src']
        result.save()

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'eCourse links have been updated.')

        return redirect('admin-ecourse-index')

    def form_invalid(self, form):
        return super().form_invalid(form)
