import json

import pytest
from apps.accounts.models import Subscription
from apps.community.api.services import (create_comment_post, delete_user_post,
                                         update_like_post, update_user_post)
from apps.community.models import Post
from apps.community.services import (create_user_post, get_all_posts,
                                     get_all_user_habits, get_following_posts)
from django.test import RequestFactory


@pytest.mark.django_db
class TestCommunityServices:
    def test_get_all_posts(self, post_factory):
        '''Тест получения всех постов'''
        post1 = post_factory()
        post2 = post_factory()
        post3 = post_factory()

        posts = get_all_posts()

        assert len(posts) == 3
        assert post3 in posts
        assert post2 in posts
        assert post1 in posts

    def test_get_following_posts(self, user_factory, post_factory):
        '''Тест получения постов пользователей, на которых подписан тестовый пользователь'''
        user = user_factory()
        following_user1 = user_factory()
        following_user2 = user_factory()
        non_following_user = user_factory()

        Subscription.objects.create(follower=user, following=following_user1)
        Subscription.objects.create(follower=user, following=following_user2)

        post1 = post_factory(user=following_user1)
        post2 = post_factory(user=following_user2)
        post_factory(user=non_following_user) 

        request = RequestFactory().get("/")
        request.user = user

        posts = get_following_posts(request)

        assert len(posts) == 2
        assert post1 in posts
        assert post2 in posts

    def test_get_all_user_habits(self, user_factory, habit_factory):
        '''Тест получения всех привычек пользователя'''
        user = user_factory()
        other_user = user_factory()

        habit1 = habit_factory(user=user)
        habit2 = habit_factory(user=user)
        habit_factory(user=other_user) 

        request = RequestFactory().get("/")
        request.user = user

        habits = get_all_user_habits(request)

        assert len(habits) == 2
        assert habit1 in habits
        assert habit2 in habits

    def test_create_user_post(self, user_factory, habit_factory):
        '''Тест создания поста'''
        user = user_factory()
        habit = habit_factory()

        post = create_user_post(
            title="Тестовый пост",
            content="Тестовое содержание",
            image=None,
            user=user,
            habit=habit,
        )

        assert post.title == "Тестовый пост"
        assert post.content == "Тестовое содержание"
        assert post.user == user
        assert post.habit == habit


@pytest.mark.django_db
class TestCommunityServicesApi:
    def test_update_like_post(self, user_factory, post_factory):
        '''Тест обновления лайка поста'''
        user = user_factory()
        post = post_factory()

        request = RequestFactory().post("/")
        request.user = user

        response = update_like_post(request, post.id)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["like"] == 1

     
        response = update_like_post(request, post.id)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["like"] == 0

    def test_create_comment_post(self, user_factory, post_factory):
        '''Тест создания комментария к посту'''
        user = user_factory()
        post = post_factory()

        request = RequestFactory().post("/")
        request.user = user
        request.data = {"content": "Тестовый комментарий"}

        response = create_comment_post(request, post.id)
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["comment"] == "Тестовый комментарий"

    def test_update_user_post(self, user_factory, post_factory):
        '''Тест обновления поста'''
        user = user_factory()
        post = post_factory(user=user)

        request = RequestFactory().put("/")
        request.user = user
        request.data = {
            "title": "Обновленный заголовок",
            "content": "Обновленное содержание",
        }

        response = update_user_post(request, post.id)
        assert response.status_code == 200

        updated_post = Post.objects.get(id=post.id)
        assert updated_post.title == "Обновленный заголовок"
        assert updated_post.content == "Обновленное содержание"

    def test_delete_user_post(self, user_factory, post_factory):
        '''Тест удаления поста'''
        user = user_factory()
        post = post_factory(user=user)

        request = RequestFactory().delete("/")
        request.user = user

        response = delete_user_post(request, post.id)
        assert response.status_code == 204

        with pytest.raises(Post.DoesNotExist):
            Post.objects.get(id=post.id)
