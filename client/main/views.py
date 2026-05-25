from django.views import generic


class Index(generic.TemplateView):
    """
    Client - Main - Index
    """

    template_name = 'client/main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = ('Biker Training offers Florida approved motorcycle safety courses including the '
                                  'Basic RiderCourse, 3‑Wheel Basic RiderCourse, and Skilled RiderCourse.')
        context['keywords'] = ('motorcycle training, Florida motorcycle license, Basic RiderCourse, '
                               '3-Wheel motorcycle course, Skilled RiderCourse, MSF training, Pensacola motorcycle class')
        context['title'] = 'Florida Motorcycle Safety Courses'

        return context
