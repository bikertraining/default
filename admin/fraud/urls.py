from django.urls import path

from admin.fraud import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='admin-fraud-index'
    ),
    path(
        'create',
        views.Create.as_view(),
        name='admin-fraud-create'
    ),
    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='admin-fraud-edit'
    ),
    path(
        '<int:pk>/delete',
        views.Delete.as_view(),
        name='admin-fraud-delete'
    ),
]
