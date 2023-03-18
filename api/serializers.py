from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class AccountSerializer(serializers.ModelSerializer):
  user_name = serializers.CharField(source='user.username')
  class Meta:
    model = Account
    fields = ['id', 'user_name', 'full_name', 'email', 'profile_pic', 'background_pic', 'created_at']

class UpdateAccountSerializer(serializers.ModelSerializer):
  class Meta:
    model = Account
    fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
  user_name = serializers.CharField(source='user_id.user.username', required=False)
  profile = serializers.ImageField(source='user_id.profile_pic', required=False)
  class Meta:
    model = Post
    fields = '__all__'

class CreatePostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
  class Meta:
    model = Follow
    fields = '__all__'

class NewFollowSerializer(serializers.ModelSerializer):
  class Meta:
    model = Follow
    fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
  user_name = serializers.CharField(source='user_id.user.username')
  class Meta:
    model = Comment
    fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Like
    fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
  # image =  serializers.CharField(source='user_id.user.username')
  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password']


