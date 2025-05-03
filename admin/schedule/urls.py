from django.urls import path

from admin.schedule import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='admin-schedule-index'
    ),
    path(
        'create',
        views.Create.as_view(),
        name='admin-schedule-create'
    ),
    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='admin-schedule-edit'
    ),
    path(
        '<int:pk>/delete',
        views.Delete.as_view(),
        name='admin-schedule-delete'
    ),
    path(
        '<int:pk>/<int:student_pk>/print',
        views.Print.as_view(),
        name='admin-schedule-print'
    ),
]
