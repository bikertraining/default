from django.views import generic

from client.schedule import models


class Index(generic.ListView):
    """
    Client - Schedule - Index
    """

    template_name = 'client/schedule/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'View upcoming motorcycle training classes including the Basic RiderCourse, 3‑Wheel Course, and Skilled RiderCourse. Check availability and reserve your spot.'
        context['keywords'] = 'motorcycle training schedule, rider course schedule, motorcycle class dates, Basic RiderCourse schedule, 3 wheel motorcycle course, skilled rider course'
        context['title'] = 'Motorcycle Training Schedule'
        context['class_type'] = self.kwargs['class_type'] if self.kwargs else None

        return context

    def get_queryset(self):
        if self.kwargs:
            return models.Schedule.objects.filter(price__class_type=self.kwargs['class_type']).order_by('date_from')

        return models.Schedule.objects.all().order_by('date_from')
