from django.urls import path

from client.courses import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-courses-index'
    ),
    path(
        '3wbrc',
        views.Brc3W.as_view(),
        name='client-courses-3wbrc'
    ),
    path(
        'brc',
        views.Brc.as_view(),
        name='client-courses-brc'
    ),
    path(
        'kickstart',
        views.Kickstart.as_view(),
        name='client-courses-kickstart'
    ),
    path(
        'private',
        views.Private.as_view(),
        name='client-courses-private'
    ),
    path(
        'src',
        views.Src.as_view(),
        name='client-courses-src'
    ),
]
