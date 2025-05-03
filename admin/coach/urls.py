from django.urls import path

from admin.coach import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='admin-coach-index'
    ),
    path(
        'create',
        views.Create.as_view(),
        name='admin-coach-create'
    ),
    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='admin-coach-edit'
    ),
    path(
        '<int:pk>/delete',
        views.Delete.as_view(),
        name='admin-coach-delete'
    ),
    path(
        'inactive',
        views.Inactive.as_view(),
        name='admin-coach-inactive'
    ),
]
