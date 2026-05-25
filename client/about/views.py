from django.views import generic


class Index(generic.TemplateView):
    """
    Client - About - Index
    """

    template_name = 'client/about/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = ('Learn about Biker Training  Motorcycle Training, our mission, '
                                  'certified instructors, rider safety philosophy, and commitment to '
                                  'high‑quality motorcycle education.')
        context['keywords'] = ('about biker training, motorcycle training instructors, rider education, '
                               'motorcycle safety school, rider training mission')
        context['title'] = 'About Biker Training LLC | Rider Education & Safety'

        return context
