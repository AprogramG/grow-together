from apps.community.models import Comment, Like, Post
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response



def update_like_post(request, post_id):
    """Функция для обновления лайка поста"""
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    like = Like.objects.filter(user=request.user, post_id=post_id)
    if like:
        like.delete()
        return JsonResponse({"like": Like.objects.filter(post_id=post_id).count()})
    else:
        Like.objects.create(user=request.user, post_id=post_id)
        return JsonResponse({"like": Like.objects.filter(post_id=post_id).count()})


def create_comment_post(request, post_id):
    """Функция для создания комментария к посту"""
    
    content = request.data.get("content")
    post = Post.objects.get(id=post_id)
    Comment.objects.create(user=request.user, post=post, content=content)
    return JsonResponse({"comment": content})



def update_user_post(request, post_id):
    """Функция для обновления поста"""
    try:
        post = Post.objects.get(id=post_id, user=request.user)
        title = request.data.get("title")
        content = request.data.get("content")
        post.title = title
        post.content = content
        post.save()
        return Response(status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



def delete_user_post(request, post_id):
    """Функция для удаления поста"""
    try:
        post = Post.objects.get(id=post_id, user=request.user)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
