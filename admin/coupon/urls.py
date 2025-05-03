from django.urls import path

from admin.coupon import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='admin-coupon-index'
    ),
    path(
        'create',
        views.Create.as_view(),
        name='admin-coupon-create'
    ),
    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='admin-coupon-edit'
    ),
    path(
        '<int:pk>/delete',
        views.Delete.as_view(),
        name='admin-coupon-delete'
    ),
]
