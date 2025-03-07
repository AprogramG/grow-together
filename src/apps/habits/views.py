from apps.habits.services.achievements import user_achievement_progress
from apps.habits.services.calendar import (current_streak,
                                           generate_calendar_data,
                                           get_day_word)
from apps.habits.services.habits import (create_user_habit,
                                         get_all_user_hbaits,
                                         get_incomplete_user_habits)
from django.shortcuts import redirect, render, reverse


def auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:login"))
        return view_func(request, *args, **kwargs)

    return wrapper


@auth_required
def home(request):
    return render(
        request,
        "habit/home.html",
        {
            "calendar_data": generate_calendar_data(request),
            "streaks": current_streak(request),
            "habits": get_incomplete_user_habits(request),
            "achievements": user_achievement_progress(request),
            "day_word": get_day_word(current_streak(request)),
        },
    )


@auth_required
def my_habits(request):

    return render(
        request, "habit/my_habits.html", {"habits": get_all_user_hbaits(request)}
    )


@auth_required
def create_habit(request):

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        create_user_habit(request, name, description)
        return redirect(reverse("my_habits"))
    return render(request, "habit/create_habit.html")
