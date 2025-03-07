import pytest
from apps.accounts.models import Subscription, User
from django.db import IntegrityError


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        '''Тест создания пользователя'''
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.completed_habits == 0
        assert user.best_streak == 0
        assert user.description == ""

    def test_update_user_stats(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        user.completed_habits = 5
        user.best_streak = 10
        user.save()

        updated_user = User.objects.get(id=user.id)
        assert updated_user.completed_habits == 5
        assert updated_user.best_streak == 10


@pytest.mark.django_db
class TestSubscriptionModel:
    def test_create_subscription(self):
        '''Тест создания подписки'''
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")

        subscription = Subscription.objects.create(follower=user1, following=user2)

        assert subscription.follower == user1
        assert subscription.following == user2

    def test_unique_subscription(self):
        '''Тест уникальности подписки'''
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")

        Subscription.objects.create(follower=user1, following=user2)

        with pytest.raises(IntegrityError):
            Subscription.objects.create(follower=user1, following=user2)

    def test_delete_subscription(self):
        '''Тест удаления подписки'''
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")

        subscription = Subscription.objects.create(follower=user1, following=user2)

        subscription.delete()
        assert not Subscription.objects.filter(follower=user1, following=user2).exists()
