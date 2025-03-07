from apps.habits.views import auth_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Habit
from .services import (create_user_post, get_all_posts, get_all_user_habits,
                       get_following_posts)


@auth_required
def community_home_page(request):

    return render(request, "community/index.html", {"posts": get_all_posts()})


@auth_required
def following_page(request):
    print(get_following_posts(request=request))
    return render(
        request, "community/following.html", {"posts": get_following_posts(request), "following": True}
    )


@auth_required
def create_post(request):
    if request.method == "POST":
        habit_id = request.POST.get("habit")
        habit = get_object_or_404(Habit, id=habit_id) if habit_id else None
        create_user_post(
            request.POST.get("title"),
            request.POST.get("content"),
            request.FILES.get("image"),
            request.user,
            habit,
        )
        return redirect("community:community_home_page")

    return render(
        request, "community/create_post.html", {"habits": get_all_user_habits(request)}
    )
