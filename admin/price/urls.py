from django.urls import path

from admin.price import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='admin-price-index'
    ),
    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='admin-price-edit'
    ),
]
