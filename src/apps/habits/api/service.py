from apps.accounts.models import User
from apps.habits.models import Calendar, Habit
from apps.habits.services.achievements import (update_achievements_status,
                                               user_achievement_progress)
from apps.habits.services.calendar import current_streak
from rest_framework import status
from rest_framework.response import Response


def update_habit(request, habit_id):
    """Обновляет привычку пользователя"""
    
    data = request.data
    habit = Habit.objects.get(id=habit_id)
    print(f"Received data: {data['name']}, {data['description']}")

    habit.name = data["name"]
    habit.description = data["description"]
    habit.save()

    return Response(status=status.HTTP_200_OK)


def delete_habit(request, habit_id):
    """Удаляет привычку пользователя"""
    habit = Habit.objects.get(id=habit_id)
    habit.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def mark_habit_as_completed(request, habit_id):
    """Отмечает привычку как выполненную"""

    habit = Habit.objects.get(id=habit_id)
    if habit.user.id != request.user.id:
        return Response(
            {"error": "You don't have permission to modify this habit"},
            status=status.HTTP_403_FORBIDDEN,
        )

    habit.is_completed = True
    habit.save()
    user = User.objects.get(id=request.user.id)
    user.completed_habits += 1
    user.save()
    habits_is_completed = Habit.objects.filter(
        user=request.user.id,
        is_completed=True,
    ).count()
    habits = Habit.objects.filter(user=request.user.id).count()
    calendar = Calendar.objects.get(user=request.user.id)
    update_achievements_status(request)
    # Если все привычки выполнены и стрик не активен, то активируем стрик
    if habits == habits_is_completed and calendar.is_streak is False:
        calendar.is_streak = True
        calendar.save()
        calendar.refresh_from_db()
        update_achievements_status(request)

        if current_streak(request) > user.best_streak:
            user.best_streak += 1
            user.save()

        return Response(
            {
                "all_is_completed": True,
                "streaks": current_streak(request),
                "achievements": user_achievement_progress(request),
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {
            "all_is_completed": False,
            "streaks": current_streak(request),
            "achievements": user_achievement_progress(request),
        },
        status=status.HTTP_200_OK,
    )
