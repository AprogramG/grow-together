import pytest
from apps.accounts.api.services import toggle_user_subscription
from apps.accounts.models import Subscription
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory

User = get_user_model()


@pytest.mark.django_db
class TestToggleUserSubscription:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")

    def test_create_subscription(self):
        request = self.factory.post("/api/subscribe/")
        request.user = self.user1

        response = toggle_user_subscription(request, self.user2.id)

        assert response.status_code == status.HTTP_201_CREATED
        assert Subscription.objects.filter(
            follower=self.user1, following=self.user2
        ).exists()

    def test_delete_subscription(self):
        # Create initial subscription
        Subscription.objects.create(follower=self.user1, following=self.user2)

        request = self.factory.post("/api/subscribe/")
        request.user = self.user1

        response = toggle_user_subscription(request, self.user2.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Subscription.objects.filter(
            follower=self.user1, following=self.user2
        ).exists()

    def test_toggle_subscription_twice(self):
        request = self.factory.post("/api/subscribe/")
        request.user = self.user1

        # First toggle - create subscription
        response1 = toggle_user_subscription(request, self.user2.id)
        assert response1.status_code == status.HTTP_201_CREATED
        assert Subscription.objects.filter(
            follower=self.user1, following=self.user2
        ).exists()

        # Second toggle - delete subscription
        response2 = toggle_user_subscription(request, self.user2.id)
        assert response2.status_code == status.HTTP_204_NO_CONTENT
        assert not Subscription.objects.filter(
            follower=self.user1, following=self.user2
        ).exists()
