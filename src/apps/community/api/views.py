
from rest_framework.decorators import api_view

from .services import (create_comment_post, delete_user_post, update_like_post,
                       update_user_post)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@permission_classes([IsAuthenticated])
@api_view(["PATCH"])
def like_post(request, post_id):
    return update_like_post(request, post_id)

@permission_classes([IsAuthenticated])
@api_view(["POST"])
def comment_post(request, post_id):
    return create_comment_post(request, post_id)

@permission_classes([IsAuthenticated])
@api_view(["PUT", "DELETE"])
def update_post(request, post_id):
    if request.method == "PUT":
        return update_user_post(request, post_id)
    elif request.method == "DELETE":
        return delete_user_post(request, post_id)
