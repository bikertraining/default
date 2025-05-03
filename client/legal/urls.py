from django.urls import path

from client.legal import views

urlpatterns = [
    path(
        'privacy',
        views.Privacy.as_view(),
        name='client-legal-privacy'
    ),
    path(
        'tos',
        views.Tos.as_view(),
        name='client-legal-tos'
    ),
]
