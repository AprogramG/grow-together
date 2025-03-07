from django.urls import path

from . import views

app_name = "community_api"

urlpatterns = [
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
]
