from django.urls import path

from client.main import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-main-index'
    ),
]
