from django.urls import path

from . import views

app_name = "community_api"

urlpatterns = [
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("comment/<int:post_id>/", views.comment_post, name="comment_post"),
    path("post/<int:post_id>/", views.update_post, name="update_post"),
]
