from datetime import datetime

from apps.habits.models import Calendar, Habit
from celery import shared_task


@shared_task
def reset_habits_status():
    """Сбрасывает статус всех привычек для всех пользователей"""
    habits = Habit.objects.all()
    habits.update(is_completed=False)
    return True

   


@shared_task
def calendar_update():
    """Обновляет календарь для всех пользователей"""
    calendars = Calendar.objects.all()
    for calendar in calendars:
        calendar.last_date = datetime.now().date()
        if calendar.is_streak:
            print(calendar.last_date)
            calendar.is_streak = False
            calendar.save()
        else:
            calendar.first_date = calendar.last_date
            calendar.save()
    return True
