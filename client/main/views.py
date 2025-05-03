from django.views import generic


class Index(generic.TemplateView):
    """
    Client - Main - Index
    """

    template_name = 'client/main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Learn to ride or improve your motorcycle skills. Get your ticket to ride!'
        context[
            'keywords'] = 'motorcycle class near me, learn to ride, msf basic rider course, motorcycle class pensacola, biker training'
        context['title'] = 'Home'

        return context
