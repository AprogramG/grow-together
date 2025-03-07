from datetime import date, datetime, timedelta

import pytest
from apps.habits.api.service import (delete_habit, mark_habit_as_completed,
                                     update_habit)
from apps.habits.models import Achievement, Calendar, Habit, User
from apps.habits.services.achievements import user_achievement_progress
from apps.habits.services.calendar import (current_streak,
                                           generate_calendar_data,
                                           get_day_word)
from apps.habits.services.habits import (create_user_habit,
                                         get_all_user_hbaits,
                                         get_incomplete_user_habits)


@pytest.mark.django_db
class TestHabitServices:
    def test_create_habit_service(self, rf, test_user):
        """Тест создания привычки"""
        request = rf.post("/")
        request.user = test_user

        result = create_user_habit(request, "Тестовая привычка", "Тестовое описание")
        assert result is True
        assert Habit.objects.filter(name="Тестовая привычка").exists()

    def test_get_all_habits(self, rf, test_user, test_habit):
        """Тест получения всех привычек"""
       

        request = rf.get("/")
        request.user = test_user


        habits = get_all_user_hbaits(request)
        assert len(habits) == 1
        assert habits[0].name == "Тестовая привычка"

    def test_get_incomplete_habits(self, rf, test_user, test_habits_one_completed):
        """Тест получения невыполненных привычек"""
        request = rf.get("/")
        request.user = test_user

        habits = get_incomplete_user_habits(request)

        assert len(habits) == 2
        assert habits[0].name == "Тестовая привычка 3"
        assert habits[1].name == "Тестовая привычка 2"


@pytest.mark.django_db
class TestCalendarService:
    def test_generate_calendar_data(self, rf, test_user):
        """Тест генерации календарных данных"""
        request = rf.get("/")
        request.user = test_user

        calendar_data = generate_calendar_data(request)

        assert "weeks" in calendar_data

        current_day = datetime.now().day
        result = []
        for week in calendar_data["weeks"]:
            for day in week:
                if (
                    day["day"] == 1
                    and day["class"] == "bg-secondary bg-opacity-25 text-white-75"
                ):
                    result.append(day)
                elif (
                    day["day"] == current_day
                    and day["class"] == "bg-secondary bg-opacity-75"
                ):
                    result.append(day)

        if current_day != 1:
            assert result[0]["class"] == "bg-secondary bg-opacity-25 text-white-75"
            assert result[1]["class"] == "bg-secondary bg-opacity-75"

        else:
            assert result[0]["class"] == "bg-secondary bg-opacity-75"

    def test_current_streak_service(self, rf, test_user):
        request = rf.get("/")
        request.user = test_user

        start_date = date.today() - timedelta(days=5)
        Calendar.objects.create(
            user=test_user,
            first_date=start_date,
            last_date=date.today(),
            is_streak=True,
        )

        streak_days = current_streak(request)
        assert streak_days == 6

    def test_day_word_declension(self):
        assert get_day_word(1) == "день"
        assert get_day_word(2) == "дня"
        assert get_day_word(5) == "дней"
        assert get_day_word(11) == "дней"
        assert get_day_word(21) == "день"


@pytest.mark.django_db
class TestAchievementsService:
    def test_user_achievement_progress(self, rf, test_user):
        """Тест проверки прогресса достижений пользователя"""
        request = rf.get("/")
        request.user = test_user

        achievement = Achievement.objects.create(
            name="Тестовое достижение", description="Описание", type="habits", target=3
        )

        for i in range(2):
            Habit.objects.create(
                user=test_user, name=f"Привычка {i}", description="Описание"
            )

        progress = user_achievement_progress(request)
        assert len(progress) == 1
        assert progress[0]["progress"] == "66.66666666666666%"
        assert progress[0]["current_value"] == 2


@pytest.mark.django_db
class TestHabitsServiceAPI:
    def test_update_habit(self, rf, test_user, test_habit):
        """Тест обновления привычки"""
        request = rf.put("/")
        request.user = test_user
        request.data = {
            "name": "Обновленная привычка",
            "description": "Обновленное описание",
        }

        response = update_habit(request, test_habit.id)
        test_habit.refresh_from_db()

        assert response.status_code == 200
        assert test_habit.name == "Обновленная привычка"
        assert test_habit.description == "Обновленное описание"

    def test_delete_habit(self, rf, test_user, test_habit):
        """Тест удаления привычки"""
        request = rf.delete("/")
        request.user = test_user

        response = delete_habit(request, test_habit.id)

        assert response.status_code == 204
        assert not Habit.objects.filter(id=test_habit.id).exists()

    def test_mark_habit_as_completed(self, rf, test_user, test_habit, test_calendar):
        """Тест отметки привычки как выполненной"""
        request = rf.patch("/")
        request.user = test_user

        response = mark_habit_as_completed(request, test_habit.id)
        test_habit.refresh_from_db()
        test_user.refresh_from_db()

        assert response.status_code == 200
        assert test_habit.is_completed is True
        assert test_user.completed_habits == 1
        assert "streaks" in response.data
        assert "achievements" in response.data

    def test_mark_habit_as_completed_unauthorized(
        self, rf, test_habit
    ):
        """Тест отметки привычки как выполненной для неавторизованного пользователя"""
        other_user = User.objects.create_user(username="other_user", password="test123")
        request = rf.patch("/")
        request.user = other_user

        response = mark_habit_as_completed(request, test_habit.id)

        assert response.status_code == 403
        assert (
            response.data["error"] == "You don't have permission to modify this habit"
        )

    def test_mark_habit_as_completed_all_habits(self, rf, test_user):
        """Тест отметки всех привычек как выполненных"""
        request = rf.patch("/")
        request.user = test_user

        Calendar.objects.create(user=test_user, is_streak=False)

        habit1 = Habit.objects.create(user=test_user, name="Привычка 1")
        habit2 = Habit.objects.create(user=test_user, name="Привычка 2")

        mark_habit_as_completed(request, habit1.id)
        response = mark_habit_as_completed(request, habit2.id)

        calendar = Calendar.objects.get(user=test_user)

        assert response.status_code == 200
        assert response.data["all_is_completed"] is True
        assert calendar.is_streak is True
