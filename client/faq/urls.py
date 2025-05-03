from django.urls import path

from client.faq import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-faq-index'
    ),
]
