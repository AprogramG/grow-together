from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователей"""

    description = models.TextField(blank=True)
    completed_habits = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)

    class Meta:
        app_label = "accounts"
        db_table = "users"
        pass


class Subscription(models.Model):
    """Модель подписок"""

    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        unique_together = ("follower", "following")
        db_table = "users_subscription"
