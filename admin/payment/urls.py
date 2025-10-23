from django.urls import path

from admin.payment import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='admin-payment-index'
    ),
    path(
        'confirmation',
        views.Confirmation.as_view(),
        name='admin-payment-confirmation'
    ),
]
