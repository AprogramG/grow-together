from datetime import timedelta
import pytest
from apps.habits.models import Calendar, Habit
from apps.accounts.models import User
from config.tasks import calendar_update, reset_habits_status
from django.utils import timezone



@pytest.mark.django_db
class TestResetHabitsStatus:
    def test_reset_habits_status_success(self):
        '''Тест сброса статуса привычек'''
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
     
        Habit.objects.create(name="Тестовая привычка 1", is_completed=True, user=user),
        Habit.objects.create(name="Тестовая привычка 2", is_completed=True, user=user),
       


        result = reset_habits_status()

        
        assert result == True
        for habit in Habit.objects.all():
            assert not habit.is_completed


@pytest.mark.django_db
class TestCalendarUpdate:
    @pytest.fixture(autouse=True)
    def setup_test(self, test_user):
        self.user = test_user

    def test_calendar_update_with_streak(self):
        '''Тест обновления календаря со стриком'''
        yesterday = timezone.now().date() - timedelta(days=1)
        calendar = Calendar.objects.create(
            user=self.user, first_date=yesterday, last_date=yesterday, is_streak=True
        )

        calendar_update()

        calendar.refresh_from_db()
        assert not calendar.is_streak
        assert calendar.last_date == timezone.now().date()
        assert calendar.first_date == yesterday

    def test_calendar_update_without_streak(self):
        '''Тест обновления календаря без стрика'''
        yesterday = timezone.now().date() - timedelta(days=1)
        calendar = Calendar.objects.create(
            user=self.user,
            first_date=yesterday,
            last_date=timezone.now().date(),
            is_streak=False,
        )

        calendar_update()

        calendar.refresh_from_db()
        assert not calendar.is_streak
        assert calendar.first_date == timezone.now().date()
        assert calendar.last_date == timezone.now().date()
