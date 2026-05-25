from django.views import generic


class Index(generic.TemplateView):
    """
    Client - Reviews - Index
    """

    template_name = 'client/reviews/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = ('Read real student reviews of Biker Training’s motorcycle safety courses in '
                                  'Florida. See why riders trust our certified MSF instructors and high‑success '
                                  'training programs.')
        context['keywords'] = ('Biker Training reviews, motorcycle course testimonials, Florida rider reviews, '
                               'MSF course feedback, Pensacola motorcycle training reviews')
        context['title'] = 'Student Reviews & Testimonials'

        return context
