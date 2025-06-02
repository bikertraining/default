from django.http import Http404
from django.views import generic

from client.courses import models


class Brc3W(generic.TemplateView):
    """
    Client - Courses - 3WBRC
    """

    template_name = 'client/courses/3wbrc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = '3-Wheel Basic Rider Course'
        context['keywords'] = '3 wheel, three wheel motorcycle class, 3 wheel motorcycle class, trike class'
        context['title'] = '3-Wheel Basic Rider Course'
        context['price'] = self.get_price()

        return context

    @staticmethod
    def get_price():
        try:
            result = models.Price.objects.get(class_type='3wbrc')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        return {
            'amount': str(result.amount),
            're_amount': str(result.re_amount)
        }


class Brc(generic.TemplateView):
    """
    Client - Courses - BRC
    """

    template_name = 'client/courses/brc.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Basic Rider Course'
        context[
            'keywords'] = 'basic rider course, basic rider course near me, motorcycle basic rider course near me, msf basic rider course'
        context['title'] = 'Basic Rider Course'
        context['price'] = self.get_price()

        return context

    @staticmethod
    def get_price():
        try:
            result = models.Price.objects.get(class_type='brc')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        return {
            'amount': str(result.amount),
            're_amount': str(result.re_amount)
        }


class Index(generic.TemplateView):
    """
    Client - Courses - Index
    """

    template_name = 'client/courses/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Motorcycle Courses'
        context['keywords'] = 'motorcycle courses, motorcycle classes near me, msf course'
        context['title'] = 'Motorcycle Courses'
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


class Kickstart(generic.TemplateView):
    """
    Client - Courses - Kickstart
    """

    template_name = 'client/courses/kickstart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Remedial Motorcycle Training'
        context['keywords'] = 'remedial motorcycle training, motorcycle, training, remedial'
        context['title'] = 'Remedial Motorcycle Training'
        context['price'] = self.get_price()

        return context

    @staticmethod
    def get_price():
        try:
            result = models.Price.objects.get(class_type='ime')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        return {
            'amount': str(result.amount)
        }


class Private(generic.TemplateView):
    """
    Client - Courses - Private
    """

    template_name = 'client/courses/private.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Private Motorcycle Lessons'
        context['keywords'] = 'private motorcycle class, private class, private'
        context['title'] = 'Private Motorcycle Lessons'
        context['price'] = self.get_price()

        return context

    @staticmethod
    def get_price():
        try:
            result = models.Price.objects.get(class_type='private')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        return {
            'amount': str(result.amount)
        }


class Src(generic.TemplateView):
    """
    Client - Courses - SRC
    """

    template_name = 'client/courses/src.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Skilled Rider Course'
        context[
            'keywords'] = 'skilled, skilled rider course, experienced rider course, motorcycle advanced rider training, msf experienced rider course'
        context['title'] = 'Skilled Rider Course'
        context['price'] = self.get_price()

        return context

    @staticmethod
    def get_price():
        try:
            result = models.Price.objects.get(class_type='src')
        except models.Price.DoesNotExist:
            raise Http404('Class Type does not exist')

        return {
            'amount': str(result.amount),
            're_amount': str(result.re_amount)
        }
