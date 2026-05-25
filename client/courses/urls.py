from django.urls import path

from client.courses import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-courses-index'
    ),
]
