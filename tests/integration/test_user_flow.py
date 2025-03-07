import json

import pytest
from apps.accounts.models import User
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestUserFlow:
    def test_user_registration(self, client):
        """Тест регистрации нового пользователя"""
        url = reverse("accounts:register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "StrongPass123!",
            "confirmation": "StrongPass123!",
        }

        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_302_FOUND
        assert User.objects.filter(username="newuser").exists()

    def test_user_login(self, client, test_user):
        """Тест входа пользователя в систему"""
        url = reverse("accounts:login")
        data = {"username": test_user.username, "password": "testpass123"}

        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_302_FOUND

    def test_profile_view(self, authenticated_client, test_user):
        """Тест просмотра профиля пользователя"""
        url = reverse("accounts:profile", kwargs={"username_id": test_user.id})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_invalid_registration(self, client):
        """Тест невалидной регистрации"""
        url = reverse("accounts:register")
        data = {
            "username": "newuser",
            "email": "invalid_email",
            "password": "weak1",
            "confirmation": "weak",
        }

        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_login(self, client):
        """Тест входа с неверными учетными данными"""
        url = reverse("accounts:login")
        data = {"username": "nonexistent", "password": "wrongpass"}

        response = client.post(url, data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
