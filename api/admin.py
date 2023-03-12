from django.contrib import admin

# Register your models here.

from .models import *

class AccountAdmin(admin.ModelAdmin):
  list_display = ['id', 'user', 'full_name']

admin.site.register(Account, AccountAdmin)

class PostAdmin(admin.ModelAdmin):
  list_display = ['id', 'user_id', 'File', 'description']

admin.site.register(Post, PostAdmin)

class FollowAdmin(admin.ModelAdmin):
  list_display = ['id', 'follower', 'followee']

admin.site.register(Follow, FollowAdmin)

class CommentAdmin(admin.ModelAdmin):
  list_display = ['id', 'text', 'post_id', 'user_id', 'created_at']

admin.site.register(Comment, CommentAdmin)

class LikeAdmin(admin.ModelAdmin):
  list_display = ['id', 'user_id', 'post_id', 'liked_by']

admin.site.register(Like, LikeAdmin)