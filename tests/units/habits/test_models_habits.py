from datetime import date

import pytest
from apps.habits.models import Achievement, Calendar, Habit


@pytest.mark.unit
class TestHabitModel:
    @pytest.mark.django_db
    def test_habit_creation(self, test_user):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            user=test_user,
            name="Тестовая привычка",
            description="Описание",
            is_completed=False,
        )
        assert str(habit) == f"{test_user}, Тестовая привычка, Описание"
        assert not habit.is_completed


@pytest.mark.unit
class TestCalendarModel:
    @pytest.mark.django_db
    def test_calendar_creation(self, test_user):
        """Тест создания календаря"""
        today = date.today()
        calendar = Calendar.objects.create(
            user=test_user, first_date=today, last_date=today, is_streak=False
        )
        assert str(calendar) == f"{test_user}, {today}, {today}"
        assert not calendar.is_streak


@pytest.mark.unit
class TestAchievementModel:
    @pytest.mark.django_db
    def test_achievement_progress_calculation(self):
        """Тест создания достижения"""
        achievement = Achievement.objects.create(
            name="Тестовое достижение", description="Описание", type="habits", target=5
        )

        assert str(achievement) == "Тестовое достижение"
        assert achievement.type == "habits"
        assert achievement.target == 5
