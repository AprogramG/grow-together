from django.urls import include, path

from . import views

app_name = "community"

urlpatterns = [
    path("", views.community_home_page, name="community_home_page"),
    path("following/", views.following_page, name="following_page"),
    path("create-post/", views.create_post, name="create_post"),
    path("api/", include("apps.community.api.urls")),
]
