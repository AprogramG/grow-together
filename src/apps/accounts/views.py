from apps.accounts.models import Subscription, User
from apps.habits.models import CompletedAchievement, Habit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect


def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse("home"), status=200)

        else:
            return render(
                request,
                "users/login.html",
                {"message": "Invalid username and/or password."},
                status=401,
            )
    else:
        return render(request, "users/login.html")


def logout_view(request):

    logout(request)
    return HttpResponseRedirect(reverse("home"))


@csrf_protect
def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(
                request,
                "users/register.html",
                {"message": "Passwords must match."},
                status=400,
            )

        try:
            validate_password(password)
        except ValidationError as e:
            return render(
                request,
                "users/register.html",
                {"message": " ".join(e.messages)},
                status=401,
            )

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "users/register.html",
                {"message": "Username already taken."},
                status=400,
            )
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "users/register.html")


def profile(request, username_id):
    try:
        user = User.objects.get(id=username_id)
        achivments = CompletedAchievement.objects.filter(user=user)
        habits_count = Habit.objects.filter(user=user).count()
        is_following = Subscription.objects.filter(
            follower=request.user, following=user
        ).exists()

        return render(
            request,
            "users/profile.html",
            {
                "user": user,
                "achievements": achivments[::-1],
                "habits_count": habits_count,
                "is_following": is_following,
            },
            status=200,
        )
    except User.DoesNotExist:
        return render(request, "users/profile.html", status=404)
