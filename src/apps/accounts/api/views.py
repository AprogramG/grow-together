from rest_framework.decorators import api_view

from .services import toggle_user_subscription


@api_view(["PATCH"])
def follow_user(request, user_id):
    return toggle_user_subscription(request, user_id)
