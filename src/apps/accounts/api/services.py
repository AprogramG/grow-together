from apps.accounts.models import Subscription, User
from rest_framework import status
from rest_framework.response import Response


def toggle_user_subscription(request, user_id):
    """Функция для подписки на пользователя"""
    if not Subscription.objects.filter(
        follower=request.user, following=user_id
    ).exists():
        user = User.objects.get(id=user_id)
        Subscription.objects.create(follower=request.user, following=user)
        return Response(status=status.HTTP_201_CREATED)
    else:
        Subscription.objects.filter(follower=request.user, following=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
