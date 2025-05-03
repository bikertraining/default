from django.urls import path
from django.views.generic import RedirectView

from client.register import views

urlpatterns = [
    path(
        '',
        RedirectView.as_view(url='/schedule'),
        name='client-register-blank'
    ),
    path(
        '<int:id>',
        views.Index.as_view(),
        name='client-register-index'
    ),
    path(
        'confirmation/<str:class_type>',
        views.Confirmation.as_view(),
        name='client-register-confirmation'
    ),
    path(
        'class-full',
        views.ClassFull.as_view(),
        name='client-register-class-full'
    ),
]
