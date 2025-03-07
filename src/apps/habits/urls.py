from django.urls import include, path

from . import views

urlpatterns = [
    path("api/", include("habits.api.urls")),
    path("", views.home, name="home"),
    path("my-habits/", views.my_habits, name="my_habits"),
    path("create-habit/", views.create_habit, name="create_habit"),
]
