from apps.habits.api.service import (delete_habit, mark_habit_as_completed,
                                     update_habit)
from rest_framework.decorators import api_view


@api_view(["PUT", "DELETE", "PATCH"])
def change_habit(request, habit_id):
    if request.method == "PUT":
        return update_habit(request, habit_id)
    elif request.method == "DELETE":
        return delete_habit(request, habit_id)
    elif request.method == "PATCH":
        return mark_habit_as_completed(request, habit_id)
