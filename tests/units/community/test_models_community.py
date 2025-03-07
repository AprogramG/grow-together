import pytest
from apps.community.models import Comment, Like, Post
from django.db import IntegrityError


@pytest.mark.django_db
class TestPost:
    def test_create_post(self, user_factory, habit_factory):
        user = user_factory()
        habit = habit_factory()

        post = Post.objects.create(
            title="Тестовый пост", content="Тестовое содержание", user=user, habit=habit
        )

        assert post.title == "Тестовый пост"
        assert post.content == "Тестовое содержание"
        assert post.user == user
        assert post.habit == habit


@pytest.mark.django_db
class TestComment:
    def test_create_comment(self, user_factory, post_factory):
        user = user_factory()
        post = post_factory()

        comment = Comment.objects.create(
            post=post, user=user, content="Тестовый комментарий"
        )

        assert comment.content == "Тестовый комментарий"
        assert comment.user == user
        assert comment.post == post


@pytest.mark.django_db
class TestLike:
    def test_create_like(self, user_factory, post_factory):
        user = user_factory()
        post = post_factory()

        like = Like.objects.create(post=post, user=user)

        assert like.user == user
        assert like.post == post

    def test_count_likes(self, user_factory, post_factory):
        user1 = user_factory()
        user2 = user_factory()
        post = post_factory()

        Like.objects.create(post=post, user=user1)
        Like.objects.create(post=post, user=user2)

        assert post.count_likes() == 2

    def test_unique_together_constraint(self, user_factory, post_factory):
        user = user_factory()
        post = post_factory()

        Like.objects.create(post=post, user=user)

        with pytest.raises(IntegrityError):
            Like.objects.create(post=post, user=user)
