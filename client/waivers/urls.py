from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        '3wbrc',
        RedirectView.as_view(url='/static/waivers/3wbrc.pdf'),
        name='client-waivers-3wbrc'
    ),
    path(
        'brc',
        RedirectView.as_view(url='/static/waivers/brc.pdf'),
        name='client-waivers-brc'
    ),
    path(
        'src',
        RedirectView.as_view(url='/static/waivers/src.pdf'),
        name='client-waivers-src'
    ),
]
