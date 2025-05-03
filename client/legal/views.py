from django.views import generic


class Privacy(generic.TemplateView):
    """
    Client - Legal - Privacy
    """

    template_name = 'client/legal/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Privacy Policy'
        context['keywords'] = 'privacy policy, privacy, policy'
        context['title'] = 'Privacy Policy'

        return context


class Tos(generic.TemplateView):
    """
    Client - Legal - Terms of Service
    """

    template_name = 'client/legal/tos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Terms of Service'
        context['keywords'] = 'tos, terms of service'
        context['title'] = 'Terms of Service'

        return context
