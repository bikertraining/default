from django.http import Http404
from django.views import generic

from client.courses import models


class Index(generic.TemplateView):
    """
    Client - Courses - Index
    """

    template_name = 'client/courses/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = ('Explore motorcycle training courses including the Basic RiderCourse, '
                                  '3‑Wheel Basic RiderCourse, and Skilled RiderCourse. Learn requirements, '
                                  'pricing, and how to register.')
        context['keywords'] = ('motorcycle training courses, Basic RiderCourse, 3 wheel motorcycle course, '
                               'skilled rider course, motorcycle safety training, rider education')
        context['title'] = 'Motorcycle Training Courses | Basic, 3‑Wheel & Skilled Rider'
        context['price'] = self.get_price()

        return context

    @staticmethod
    def get_price():
        try:
            result_brc = models.Price.objects.get(class_type='brc')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        try:
            result_3wbrc = models.Price.objects.get(class_type='3wbrc')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        try:
            result_src = models.Price.objects.get(class_type='src')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        try:
            result_ime = models.Price.objects.get(class_type='ime')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        try:
            result_private = models.Price.objects.get(class_type='private')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        return {
            'amount_brc': str(result_brc.amount),
            'amount_3wbrc': str(result_3wbrc.amount),
            'amount_src': str(result_src.amount),
            'amount_ime': str(result_ime.amount),
            'amount_private': str(result_private.amount)
        }
