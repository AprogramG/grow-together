import pytest
from apps.community.models import Comment, Like, Post
from django.urls import reverse


@pytest.mark.django_db
class TestCommunityFlow:
    def test_create_post(self, authenticated_client, user):
        """Тест создания поста"""
        post_data = {
            "title": "Тестовый заголовок",
            "content": "Тестовый контент",
        }

        response = authenticated_client.post(
            reverse("community:create_post"), data=post_data
        )

        assert response.status_code == 302  
        assert Post.objects.count() == 1
        post = Post.objects.first()
        assert post.title == post_data["title"]
        assert post.content == post_data["content"]
        assert post.user == user

    def test_create_post_with_habit(self, authenticated_client, test_user, test_habit):
        """Тест создания поста с привычкой"""
        post_data = {
            "title": "Пост с привычкой",
            "content": "Контент с привычкой",
            "habit": str(test_habit.id),
        }

        response = authenticated_client.post(
            reverse("community:create_post"), data=post_data
        )

        assert response.status_code == 302
        post = Post.objects.first()
        assert post.habit.id == test_habit.id

    def test_like_post(self, authenticated_client, test_post):
        """Тест лайка поста"""
        test_post, test_user = test_post
        response = authenticated_client.patch(
            f"/community/api/like/{test_post.id}/", content_type="application/json"
        )

        assert response.status_code == 200
        assert Like.objects.count() == 1
        like = Like.objects.first()
        assert like.post_id == test_post.id

        response = authenticated_client.patch(
            f"/community/api/like/{test_post.id}/", content_type="application/json"
        )

        assert response.status_code == 200
        assert Like.objects.count() == 0

    def test_create_comment(self, authenticated_api_client, test_post):
        """Тест создания комментария"""
        test_post, test_user = test_post
        comment_data = {"content": "Тестовый комментарий"}

        response = authenticated_api_client.post(
            f"/community/api/comment/{test_post.id}/", data=comment_data, format="json"
        )

        assert response.status_code == 200
        assert Comment.objects.count() == 1
        comment = Comment.objects.first()
        assert comment.content == comment_data["content"]
        assert comment.post_id == test_post.id

    def test_update_post(self, api_client, test_post):
        """Тест обновления поста"""
        test_post, test_user = test_post
        api_client.force_authenticate(user=test_user)
        
        update_data = {
            "title": "Обновленный заголовок",
            "content": "Обновленный контент",
        }

        response = api_client.put(
            f"/community/api/post/{test_post.id}/", data=update_data, format="json"
        )

        assert response.status_code == 200
        test_post.refresh_from_db()
        assert test_post.title == update_data["title"]
        assert test_post.content == update_data["content"]
        
    def test_update_post_unauthorized_user(self, authenticated_api_client, test_post, user_factory):
        """Тест обновления поста неавторизованным пользователем"""
        test_post, test_user = test_post
        
        update_data = {
            "title": "Обновленный заголовок",
            "content": "Обновленный контент",
        }

        response = authenticated_api_client.put(
            f"/community/api/post/{test_post.id}/", data=update_data, format="json"
        )

        assert response.status_code == 405
        
        test_post.refresh_from_db()
        assert test_post.title != update_data["title"]
        assert test_post.content != update_data["content"]

    def test_delete_post(self, api_client, test_post):
        """Тест удаления поста"""
        test_post, test_user = test_post
        api_client.force_authenticate(user=test_user)
        response = api_client.delete(
            f"/community/api/post/{test_post.id}/",
        )

        assert response.status_code == 204
        assert Post.objects.count() == 0

    def test_unauthorized_access(self, api_client, test_post):
        """Тест доступа неавторизованного пользователя"""
        test_post, test_user = test_post
        response = api_client.post(
            reverse("community:create_post"),
            data={"title": "Тест", "content": "Контент"},
        )
        assert response.status_code == 302

        response = api_client.patch(
            f'/community/api/like/{test_post.id}/',
            content_type='application/json'
        )

       
        assert 'application/json' in response['Content-Type']

    def test_community_home_page(self, authenticated_client):
        """Тест главной страницы сообщества"""
        response = authenticated_client.get(reverse("community:community_home_page"))
        assert response.status_code == 200

    def test_following_page(self, authenticated_client):
        """Тест страницы подписок"""
        response = authenticated_client.get(reverse("community:following_page"))
        assert response.status_code == 200
