from apps.habits.models import Calendar, Habit


def get_incomplete_user_habits(request: object) -> list[Habit]:
    """Возвращает список невыполненных привычек для пользователя"""
    return Habit.objects.filter(user=request.user, is_completed=False)[::-1]


def get_all_user_hbaits(request):
    """Возвращает список всех привычек для пользователя"""
    return Habit.objects.filter(user=request.user)[::-1]


def create_user_habit(request: object, name: str, description: str) -> bool:
    """Создает новую привычку"""
    if not Calendar.objects.filter(user=request.user).exists():
        Calendar.objects.create(user=request.user)
    Habit.objects.create(name=name, description=description, user=request.user)
    return True
