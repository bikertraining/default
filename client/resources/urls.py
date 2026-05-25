from django.urls import path
from django.views.generic import RedirectView

from client.resources import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-resources-index'
    ),
    path(
        'downloads/exercises/3wbrc',
        RedirectView.as_view(url='/static/resources/downloads/exercises/3wbrc.pdf'),
        name='client-resources-downloads-exercises-3wbrc'
    ),
    path(
        'downloads/exercises/brc',
        RedirectView.as_view(url='/static/resources/downloads/exercises/brc.pdf'),
        name='client-resources-downloads-exercises-brc'
    ),
    path(
        'downloads/exercises/src',
        RedirectView.as_view(url='/static/resources/downloads/exercises/src.pdf'),
        name='client-resources-downloads-exercises-src'
    ),
    path(
        'downloads/homework/brc',
        RedirectView.as_view(url='/static/resources/downloads/homework/brc.pdf'),
        name='client-resources-downloads-homework-brc'
    ),
    path(
        'downloads/homework/3wbrc',
        RedirectView.as_view(url='/static/resources/downloads/homework/3wbrc.pdf'),
        name='client-resources-downloads-homework-3wbrc'
    ),
    path(
        'downloads/tclocs',
        RedirectView.as_view(url='/static/resources/downloads/tclocs.pdf'),
        name='client-resources-downloads-tclocs'
    ),
    path(
        'downloads/waivers/3wbrc',
        RedirectView.as_view(url='/static/resources/downloads/waivers/3wbrc.pdf'),
        name='client-resources-downloads-waivers-3wbrc'
    ),
    path(
        'downloads/waivers/brc',
        RedirectView.as_view(url='/static/resources/downloads/waivers/brc.pdf'),
        name='client-resources-downloads-waivers-brc'
    ),
    path(
        'downloads/waivers/src',
        RedirectView.as_view(url='/static/resources/downloads/waivers/src.pdf'),
        name='client-resources-downloads-waivers-src'
    ),
]
