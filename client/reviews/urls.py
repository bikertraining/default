from django.urls import path

from client.reviews import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='client-reviews-index'
    ),
]
