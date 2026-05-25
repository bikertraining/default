from django.views import generic


class Index(generic.TemplateView):
    """
    Client - Resource - Index
    """

    template_name = 'client/resources/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['description'] = 'Access motorcycle training resources including safety guides, riding tips, class preparation checklists, licensing info, and downloadable materials for new riders.'
        context[
            'keywords'] = 'motorcycle training resources, rider guides, motorcycle safety tips, motorcycle class checklist, motorcycle licensing info, rider preparation'
        context['title'] = 'Motorcycle Training Resources | Guides, Checklists & Safety Tips'

        return context
