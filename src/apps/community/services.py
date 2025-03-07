from apps.accounts.models import Subscription
from apps.community.models import Post
from apps.habits.models import Habit


def get_all_posts():
    """Функция для получения всех постов"""
    return Post.objects.all()[::-1]


def get_following_posts(request):
    """Функция для получения постов пользователей, на которых подписан текущий пользователь"""
    subscription = Subscription.objects.filter(follower=request.user)
    following_user = subscription.values_list("following", flat=True)
    posts = Post.objects.filter(user__in=following_user)
    return posts[::-1]


def get_all_user_habits(request):
    """Функция для получения всех привычек пользователя"""
    return Habit.objects.filter(user=request.user)


def create_user_post(title, content, image, user, habit):
    post = Post.objects.create(
        title=title, content=content, image=image, user=user, habit=habit
    )
    return post
