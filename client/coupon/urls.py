from django.urls import path

from client.coupon import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-coupon-index'
    ),
    path(
        '<str:class_type>',
        views.Index.as_view(),
        name='client-coupon-index'
    ),
    path(
        '<str:class_type>/<str:name>',
        views.Index.as_view(),
        name='client-coupon-index'
    ),
]
