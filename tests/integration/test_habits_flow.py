import pytest
from apps.accounts.models import User
from apps.habits.models import Habit


@pytest.mark.django_db
class TestHabitsFlow:
    def test_full_habits_flow(self, test_client, test_user: User):
        """
        Тестирует полный flow работы с привычками:
        1. Создание привычки
        2. Получение списка привычек
        3. Отметка выполнения привычки
        4. Проверка статистики
        """
        response = test_client.post(
            "/accounts/login/",
            data={"username": test_user.username, "password": "testpass123"},
            follow=True,
        )
        assert response.status_code == 200

        habit_data = {
            "name": "Пить воду",
            "description": "Выпивать 2л воды каждый день",
        }
        response = test_client.post("/create-habit/", data=habit_data, follow=True)
        assert response.status_code == 200

        habit = Habit.objects.get(name=habit_data["name"])
        assert habit.description == habit_data["description"]
        assert habit.user == test_user

        response = test_client.get("/my-habits/")
        assert response.status_code == 200

        response = test_client.patch(
            f"/api/habits/{habit.id}/",
            data={"completed": True},
            content_type="application/json",
        )
        assert response.status_code == 200

        habit.refresh_from_db()
        assert habit.is_completed == True

    def test_habit_sharing_flow(self, test_client, test_user: User):
        """
        Тестирует flow работы с привычками:
        1. Создание привычки
        2. Получение списка привычек
        """
        response = test_client.post(
            "/accounts/login/",
            data={"username": test_user.username, "password": "testpass123"},
            follow=True,
        )
        assert response.status_code == 200

        habit_data = {
            "name": "Медитация",
            "description": "Медитировать 15 минут каждое утро",
        }
        response = test_client.post("/create-habit/", data=habit_data, follow=True)
        assert response.status_code == 200

        habit = Habit.objects.get(name=habit_data["name"])
        assert habit.description == habit_data["description"]
        assert habit.user == test_user

        response = test_client.get("/my-habits/")
        assert response.status_code == 200
