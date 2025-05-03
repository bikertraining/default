from django.urls import path

from client.payment import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-payment-index'
    ),
    path(
        '<str:class_type>',
        views.Payment.as_view(),
        name='client-payment-class-type'
    ),
    path(
        'confirmation/<str:class_type>',
        views.Confirmation.as_view(),
        name='client-payment-confirmation'
    ),
]
