from django.views import generic


class Privacy(generic.TemplateView):
    """
    Client - Legal - Privacy
    """

    template_name = 'client/legal/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = ('Read the Biker Training Motorcycle Training Privacy Policy to understand how we '
                                  'collect, use, and protect your information.')
        context['keywords'] = 'privacy policy, data protection, user privacy, privacy, motorcycle training privacy'
        context['title'] = 'Privacy Policy'

        return context


class Tos(generic.TemplateView):
    """
    Client - Legal - Terms of Service
    """

    template_name = 'client/legal/tos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = ('Review the Terms of Service for Biker Training LLC, including user '
                                  'responsibilities, policies, and conditions for using our website and services.')
        context['keywords'] = ('terms of service, biker training terms, motorcycle training terms, user agreement, '
                               'service policies')
        context['title'] = 'Terms of Service'

        return context
