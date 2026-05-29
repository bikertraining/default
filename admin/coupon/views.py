from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views import generic

from admin.coupon import models


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


class Create(LoginRequiredMixin, generic.CreateView):
    """
    Admin - Coupon - Create
    """

    model = models.Coupon
    fields = ['amount', 'class_type', 'is_active', 'name', 'one_time_use']
    template_name = 'admin/coupon/create.html'
    success_url = reverse_lazy('admin-coupon-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Create Coupon'
        context['keywords'] = ''
        context['title'] = 'Create Coupon'

        return context

    def form_valid(self, form):
        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Coupon has been created.')

        return super(Create, self).form_valid(form)


class Edit(LoginRequiredMixin, generic.UpdateView):
    """
    Admin - Coupon - Edit
    """

    model = models.Coupon
    fields = ['amount', 'class_type', 'is_active', 'one_time_use']
    template_name = 'admin/coupon/edit.html'
    success_url = reverse_lazy('admin-coupon-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Edit Coupon'
        context['keywords'] = ''
        context['title'] = 'Edit Coupon'

        return context

    def form_valid(self, form):
        # Update Coupon Object
        result = self.get_object()
        result.amount = form.cleaned_data['amount']
        result.class_type = form.cleaned_data['class_type']
        result.is_active = form.cleaned_data['is_active']
        result.one_time_use = form.cleaned_data['one_time_use']
        result.save()

        # Display Message
        messages.add_message(self.request, messages.SUCCESS, 'Coupon has been updated.')

        return super(Edit, self).form_valid(form)


class Delete(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    """
    Admin - Coupon - Delete
    """

    model = models.Coupon
    success_message = 'Coupon has been deleted.'

    def get_success_url(self):
        return reverse('admin-coupon-index')
