from django.urls import path

from client.about import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-about-index'
    ),
]
