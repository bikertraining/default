from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        '3wbrc',
        RedirectView.as_view(url='https://a.co/d/bTiwMvM'),
        name='client-book-3wbrc'
    ),
    path(
        'brc',
        RedirectView.as_view(url='https://a.co/d/gBUB6UM'),
        name='client-book-brc'
    ),
]
