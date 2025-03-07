from apps.accounts.models import User
from apps.habits.models import Habit
from django.db import models


class Post(models.Model):
    """Модель постов"""

    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def count_likes(self):
        return Like.objects.filter(post=self).count()


class Comment(models.Model):
    """Модель комментариев"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "post_comment"


class Like(models.Model):
    """Модель лайков"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "user")
        db_table = "post_like"
