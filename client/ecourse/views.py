from django.http import Http404
from django.views import generic

from client.ecourse import models


class Index(generic.TemplateView):
    """
    Client - eCourse - Index
    """

    template_name = 'client/ecourse/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'ePackage-1 eCourse'
        context['keywords'] = 'eCourse, msf ecourse, ePackage-1 eCourse'
        context['title'] = 'ePackage-1 eCourse'
        context['ecourse_link'] = self.get_ecourse_link()

        return context

    def get_ecourse_link(self):
        try:
            result = models.Ecourse.objects.get(pk=1)
        except models.Ecourse.DoesNotExist:
            raise Http404('Ecourse does not exist')

        if self.kwargs['class_type'] == 'brc':
            return result.link_brc
        elif self.kwargs['class_type'] == '3wbrc':
            return result.link_3wbrc
        elif self.kwargs['class_type'] == 'src':
            return result.link_src
