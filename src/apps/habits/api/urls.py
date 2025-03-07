from django.urls import path

from . import views

urlpatterns = [
    path("habits/<int:habit_id>/", views.change_habit, name="change_habit"),
]
