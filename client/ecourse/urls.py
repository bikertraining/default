from django.urls import path

from client.ecourse import views

urlpatterns = [
    path(
        '<str:class_type>',
        views.Index.as_view(),
        name='client-ecourse-index'
    ),
]
