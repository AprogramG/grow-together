from django.urls import include, path

from . import views

app_name = "accounts"

urlpatterns = [
    path("user/<int:username_id>", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("api/", include("apps.accounts.api.urls")),
]
