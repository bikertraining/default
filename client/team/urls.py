from django.urls import path

from client.team import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-team-index'
    ),
    path(
        'confirmation',
        views.Confirmation.as_view(),
        name='client-team-confirmation'
    ),
    path(
        'blocked',
        views.Blocked.as_view(),
        name='client-team-blocked'
    ),
    path(
        'faq',
        views.Faq.as_view(),
        name='client-team-faq'
    ),
]
