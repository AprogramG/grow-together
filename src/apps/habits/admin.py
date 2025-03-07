from apps.habits.models import (Achievement, Calendar, CompletedAchievement,
                                Habit)
from django.contrib import admin

admin.site.register(Calendar)

admin.site.register(Achievement)
admin.site.register(CompletedAchievement)
admin.site.register(Habit)
