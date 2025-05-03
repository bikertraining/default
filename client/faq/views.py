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
        context['description'] = 'Frequently Asked Questions'
        context['keywords'] = 'frequently asked questions, faq'
        context['title'] = 'FAQ'
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
