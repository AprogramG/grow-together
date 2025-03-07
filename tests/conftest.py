from datetime import date
import os

import pytest
from apps.accounts.models import User
from apps.community.models import Comment, Like, Post
from apps.habits.models import  Calendar, Habit
from django.test import Client, RequestFactory
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service



def create_user(**kwargs):
    """Функция для создания пользователей."""
    defaults = {
        "username": f"testuser_{timezone.now().timestamp()}",
        "email": f"test_{timezone.now().timestamp()}@example.com",
        "password": "testpass123",
    }
    defaults.update(kwargs)

    user = User.objects.create_user(
        username=defaults["username"],
        email=defaults["email"],
        password=defaults["password"],
    )
    return user


def create_habit(**kwargs):
    """Функция для создания привычек."""
    if "user" not in kwargs:
        kwargs["user"] = create_user()

    defaults = {
        "name": "Тестовая привычка",
        "description": "Тестовое описание",
        "is_completed": False,
    }
    defaults.update(kwargs)

    return Habit.objects.create(**defaults)


def create_calendar(**kwargs):
    """Функция для создания календаря."""
    if "user" not in kwargs:
        kwargs["user"] = create_user()

    defaults = {
        "first_date": date.today(),
        "last_date": date.today(),
        "is_streak": False,
    }
    defaults.update(kwargs)

    return Calendar.objects.create(**defaults)


def create_post(**kwargs):
    """Функция для создания поста."""
    if "user" not in kwargs:
        kwargs["user"] = create_user()

    defaults = {"title": "Тестовый пост", "content": "Тестовый контент", "habit": None}
    defaults.update(kwargs)

    return Post.objects.create(**defaults)


def create_comment(**kwargs):
    """Функция для создания комментария."""
    if "user" not in kwargs:
        kwargs["user"] = create_user()
    if "post" not in kwargs:
        kwargs["post"] = create_post()

    defaults = {"content": "Тестовый комментарий"}
    defaults.update(kwargs)

    return Comment.objects.create(**defaults)


def create_like(**kwargs):
    """Функция для создания лайка."""
    if "user" not in kwargs:
        kwargs["user"] = create_user()
    if "post" not in kwargs:
        kwargs["post"] = create_post()

    return Like.objects.create(**kwargs)


@pytest.fixture
def api_client():
    """Фикстура для REST API тестов."""
    return APIClient()


@pytest.fixture
def client():
    """Фикстура для Django тестов."""
    return Client()


@pytest.fixture
def user():
    """Фикстура для создания тестового пользователя."""
    return create_user()


@pytest.fixture
def authenticated_client(client, user):
    """Фикстура для аутентифицированного Django клиента."""
    client.force_login(user)
    return client


@pytest.fixture
def authenticated_api_client(api_client, user):
    """Фикстура для аутентифицированного REST API клиента."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def rf():
    """Фикстура для RequestFactory."""
    return RequestFactory()


@pytest.fixture
def test_user():
    """Создает тестового пользователя."""
    return create_user()


@pytest.fixture
def test_habit(test_user):
    """Создает тестовую привычку."""
    return create_habit(user=test_user)


@pytest.fixture
def user_factory():
    """Фикстура-фабрика для создания пользователей."""
    return create_user


@pytest.fixture
def post_factory():
    """Фикстура-фабрика для создания постов."""
    return create_post


@pytest.fixture
def habit_factory():
    """Фикстура-фабрика для создания привычек."""
    return create_habit


@pytest.fixture
def test_habits_one_completed(test_user):
    """Создает набор привычек, одна из которых выполнена."""
    habit1 = create_habit(
        user=test_user, name="Тестовая привычка 2", is_completed=False
    )
    habit2 = create_habit(
        user=test_user, name="Тестовая привычка 3", is_completed=False
    )
    return [habit1, habit2]


@pytest.fixture
def test_calendar(test_user):
    """Создает тестовый календарь."""
    return create_calendar(user=test_user)


@pytest.fixture
def test_post(test_user):
    """Создает тестовый пост."""
    return create_post(user=test_user), test_user


@pytest.fixture
def test_comment(test_user, test_post):
    """Создает тестовый комментарий."""
    return create_comment(user=test_user, post=test_post)


@pytest.fixture
def test_like(test_user, test_post):
    """Создает тестовый лайк."""
    return create_like(user=test_user, post=test_post)


@pytest.fixture
def test_client():
    """Фикстура для тестового клиента."""
    client = Client()
    return client


@pytest.fixture
def test_user_with_token(test_user):
    """Создает тестового пользователя с токеном доступа."""
    refresh = RefreshToken.for_user(test_user)
    test_user.access_token = str(refresh.access_token)
    return test_user


@pytest.fixture
def selenium_driver(request):
   
   
   
    
   
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
   
   
    
   
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)


    yield driver
    driver.quit()


@pytest.fixture
def live_server_url():
    """Фикстура для получения URL тестового сервера."""
    return "http://localhost:8000" 


