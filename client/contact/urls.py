from django.urls import path

from client.contact import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-contact-index'
    ),
    path(
        'confirmation',
        views.Confirmation.as_view(),
        name='client-contact-confirmation'
    ),
    path(
        'blocked',
        views.Blocked.as_view(),
        name='client-contact-blocked'
    ),
]
