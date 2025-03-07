from datetime import date

from apps.accounts.models import User
from django.db import models
from django.test import RequestFactory


class Achievement(models.Model):
    """Модель достижений"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    img = models.FileField(upload_to="achievements/")
    type = models.CharField(max_length=200)
    target = models.IntegerField()

    class Meta:
        app_label = "habits"
        db_table = "achievements"

    def calculate_progress(self, user):
        from apps.habits.services.calendar import current_streak

        current_value = 0

        if self.type == "streaks":
            request = RequestFactory()
            request.user = user
            current_value = current_streak(request)
        if self.type == "habits":
            current_value = Habit.objects.filter(user=user).count()
        if self.type == "completed_habits":
            current_value = User.objects.get(username=user).completed_habits
        if self.type == "achievements":
            if (
                CompletedAchievement.objects.filter(user=user).count()
                == Achievement.objects.count() - 1
            ):
                current_value = 1
            else:
                current_value = 0

        progress = min(100, (current_value / self.target) * 100)
        if current_value > self.target:
            current_value = self.target

        return {
            "progress": f"{progress}%",
            "current_value": current_value,
            "target": self.target,
        }

    def __str__(self):
        return self.name


class CompletedAchievement(models.Model):
    """Модель для отслеживания выполненных достижений пользователя"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}, {self.achievement}"

    class Meta:
        app_label = "habits"
        db_table = "achievements_completed"


class Calendar(models.Model):
    """Пользовательский календарь"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_date = models.DateField(default=date.today)
    last_date = models.DateField(default=date.today)
    is_streak = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}, {self.first_date}, {self.last_date}"

    class Meta:
        app_label = "habits"
        db_table = "calendars"


class Habit(models.Model):
    """Модель привычек"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}, {self.name}, {self.description}"

    class Meta:
        app_label = "habits"
        db_table = "habits"
        pass
