from django.urls import path
from django.views.generic import RedirectView

from client.courses import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-courses-index'
    ),
    path(
        '3wbrc',
        RedirectView.as_view(url='/courses/', permanent=True),
        name='client-courses-3wbrc'
    ),
    path(
        'brc',
        RedirectView.as_view(url='/courses/', permanent=True),
        name='client-courses-brc'
    ),
    path(
        'src',
        RedirectView.as_view(url='/courses/', permanent=True),
        name='client-courses-src'
    ),
    path(
        'kickstart',
        RedirectView.as_view(url='/courses/', permanent=True),
        name='client-courses-kickstart'
    ),
    path(
        'private',
        RedirectView.as_view(url='/courses/', permanent=True),
        name='client-courses-private'
    ),
]
