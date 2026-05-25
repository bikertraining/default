from django.http import Http404
from django.views import generic

from client.faq import models


class Index(generic.TemplateView):
    """
    Client - FAQ - Index
    """

    template_name = 'client/faq/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = ('Find answers to common questions about motorcycle training, licensing, scheduling, '
                                  'requirements, payments, and what to expect on class day.')
        context['keywords'] = ('keywords" content="motorcycle training FAQ, rider course questions, '
                               'motorcycle license questions, Basic RiderCourse FAQ, motorcycle class requirements, '
                               'motorcycle training info')
        context['title'] = 'FAQ – Motorcycle Training Questions & Answers'
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

        return {
            'process_amount_brc': str(result_brc.process_amount),
            're_amount_brc': str(result_brc.re_amount),
            'process_amount_3wbrc': str(result_3wbrc.process_amount),
            're_amount_3wbrc': str(result_3wbrc.re_amount),
            'process_amount_src': str(result_src.process_amount),
            're_amount_src': str(result_src.re_amount)
        }
