from django.contrib import admin

from .models import Comment, Like, Post

# Register your models here.
admin.site.register(Post)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "content", "created_at")


admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
