from django.urls import path

from client.schedule import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-schedule-index'
    ),
    path(
        '<str:class_type>',
        views.Index.as_view(),
        name='client-schedule-class-type'
    ),
]
