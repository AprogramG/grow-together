from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from config.tasks import calendar_update, reset_habits_status
from django.test import override_settings
from django.utils import timezone


@pytest.mark.django_db
class TestCeleryIntegration:

    @pytest.fixture
    def mock_celery_app(self):
        with patch("celery.app.task.Task.delay") as mock_delay:
            mock_delay.return_value = True
            yield mock_delay

    def test_reset_habits_status_task(self, mock_celery_app):
        '''Тест проверяет корректность вызова задачи сброса статуса привычек'''
        
        result = reset_habits_status.delay()

        mock_celery_app.assert_called_once_with()
        assert result is True

    def test_calendar_update_task(self, mock_celery_app):
        '''Тест проверяет корректность вызова задачи обновления календаря'''
        
        result = calendar_update.delay()

        # Проверяем, что задача была вызвана без параметров
        mock_celery_app.assert_called_once_with()
        assert result is True

   
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_habit_reset_integration(self, test_habit):
        '''Интеграционный тест для проверки сброса статуса привычек'''
        
        test_habit.is_completed = True
        test_habit.save()

        result = reset_habits_status()

     
        assert result is not None

        test_habit.refresh_from_db()

        assert test_habit.is_completed is False

    
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_calendar_update_integration(self, test_calendar):
        '''Интеграционный тест для проверки обновления календаря'''
        
        initial_date = timezone.now().date() - timedelta(days=1)
        test_calendar.last_date = initial_date
        test_calendar.save()

        # Запускаем задачу
        calendar_update()

        # Обновляем календарь из базы данных
        test_calendar.refresh_from_db()

        # Проверяем, что дата календаря обновилась
        assert test_calendar.last_date != initial_date
        assert test_calendar.last_date == timezone.now().date()
