from django.urls import path

from admin.ecourse import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='admin-ecourse-index'
    ),
]
