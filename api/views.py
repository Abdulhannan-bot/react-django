from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
 
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


from .serializers import *
from .models import *
from .decorators import *

# Create your views here.

# class CustomAuthToken(ObtainAuthToken):
#   def post(self, request, *args, **kwargs):
#     serializer = self.serializer_class(data=request.data,context={'request': request})
#     serializer.is_valid(raise_exception=True)
#     user = serializer.validated_data['user']
#     token, created = Token.objects.get_or_create(user=user)
#     return Response({
#       'token': token.key,
#       'user_id': user.pk,
#       'email': user.email
#   })



# @allowed_users(allowed_roles=['admin'])
@api_view(['GET'])
def apiOverview(request):
  api_urls = {
    'Accounts': '/accounts/',
    'Account Detail': '/account-detail/<str:id>',
    'Create Account': '/account-create/',
    'Update Account': '/account-update/<str:id>',
    'Delete Account': '/account-delete/<str:id>',

    'Posts': '/posts/',
    'Post Detail': '/post-detail/<str:id>',
    'Create Post': '/post-create/',
    'Delete Post': '/post-delete/<str:id>',

    'Follows': '/follows/',
    'Follow': '/follow/<str:id>',
    'UnFollow': '/unfollow/<str:id>',

    'Likes': '/likes/',
    'Like': '/like/<str:id>',
    'Unlike': '/unlike/<str:id>',

    'Comments': '/comments/',
    'Add Comment': '/add-cooment/',
  }

  return Response(api_urls)

########################################################################################################################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accounts(request):
  accounts = Account.objects.all()
  serializers = AccountSerializer(accounts, many=True)
  return Response(serializers.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def account_detail(request, *args, **kwargs):
  print(request.user)
  token = Token.objects.get(key = kwargs.get("key"))
  account = Account.objects.get(user = token.user)
  follows = Follow.objects.all()
  exclude_list = [token.user]
  excl_list = []
  account_list = [account]
  my_follows = []
  for i in follows:
    print(str(i.followee))
    if(str(i.follower) == str(token.user.account)):
      # my_follows.append(Account.objects.get(id = i.follower_id))
      user_instance = User.objects.get(username = str(i.followee.user.username))
      account_instance = Account.objects.get(user = user_instance)
      exclude_list.append(user_instance)
      excl_list.append(user_instance)
      account_list.append(account_instance)
  # print(my_follows)
  my_follows_account = Account.objects.filter(user_id__in = excl_list);
  accounts = Account.objects.exclude(user__in = exclude_list)
  print(accounts.count())
  count = Post.objects.filter(user_id__in = account_list).count()
  posts = reversed(Post.objects.filter(user_id__in = account_list).order_by('created_at'))
  following = Follow.objects.filter(follower_id = account)
  follower = Follow.objects.filter(followee_id = account)
  likes = Like.objects.filter(liked_by = token.user.account) 
  my_likes = Like.objects.filter(user_id = token.user.account)
  my_posts = Post.objects.filter(user_id = token.user.account).order_by('created_at')
  
  my_post_list = []
  for i in my_posts:
    if i.File is not None:
      print("yes")
      my_post_list.append(i)
  print(my_post_list)
  print(my_posts)

  serializers_myfollow = AccountSerializer(my_follows_account, many=True)
  serializers = AccountSerializer(account, many=False)
  serializers_suggestions = AccountSerializer(accounts, many=True)
  serializers_posts = PostSerializer(posts, many=True)
  serializers_following = FollowSerializer(following, many=True)
  serializers_followers = FollowSerializer(follower, many=True)
  serializers_likes = LikeSerializer(likes, many=True)
  serializers_mylikes = LikeSerializer(my_likes, many=True)
  serializers_myposts = PostSerializer(my_posts, many = True)

  return Response(
    {
    'suggestions': serializers_suggestions.data,
    'posts': serializers_posts.data,
    'following': serializers_following.data,
    'followers': serializers_followers.data,
    'likes': serializers_likes.data,
    'my_like': serializers_mylikes.data,
    'my_posts': serializers_myposts.data,
    'my_follows': serializers_myfollow.data,
    })

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def account_info(request, *args, **kwargs):
  token = Token.objects.get(key = kwargs.get("key"))
  id = kwargs.get("id")
  my_account = Account.objects.get(user = token.user)
  print(my_account.full_name)
  account = Account.objects.get(id = id)
  followings = Follow.objects.filter(follower_id = account)
  followers = Follow.objects.filter(followee_id = account)
  likes = Like.objects.filter(user_id = account) 
  posts = Post.objects.filter(user_id = account)
  testing = Follow.objects.filter(follower_id = my_account, followee_id = account)
  # if Follow.objects.filter(follower_id = my_account).exists():
  # if Follow.objects.filter(follower_id = my_account).exists():
  #   follows = Follow.objects.filter(follower_id = my_account)
  #   serializers_follow = FollowSerializer(follows, many=False)
  #   follows = serializers_follow.data
  # else:
  #   follows = {}

  # print(follows)
  serializers_account = UpdateAccountSerializer(account, many=False),
  serializers_posts = PostSerializer(posts, many=True)
  serializers_following = FollowSerializer(followings, many=True)
  serializers_followers = FollowSerializer(followers, many=True)
  serializers_likes = LikeSerializer(likes, many=True)
  serializers_follow = FollowSerializer(testing, many=True)
  
  return Response({
    'following': serializers_followers.data,
    'followers': serializers_following.data,
    'likes': serializers_likes.data,
    'follows': serializers_follow.data,
    'posts': serializers_posts.data,
    'cover': str(account.background_pic),
    'profile': str(account.profile_pic),
    'username': account.user.username,
    'name': account.full_name,
    'email': account.email,
    'account': account.id
  })



@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def account_update(request,id):
  # token = Token.objects.get(key = kwargs.get("key"))
  # account = Account.objects.get(user = token.user)
  account = Account.objects.get(id = id)
  print(request.data.get("background_pic"))
  print(request.data.get("profile_pic"))
  print(request.data.get("full_name"))
  print(request.data.get("email"))
  print(request.data.get("user"))
  serializers = UpdateAccountSerializer(instance = account, data = request.data)
  if serializers.is_valid():
    serializers.save()
  return Response(serializers.data)

@api_view(['POST'])
def account_create(request):
  serializers = AccountSerializer(data = request.data)
  if serializers.is_valid():
    serializers.save()
  return Response(serializers.data)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def account_delete(request, id):
  account = Account.objects.get(id = id)
  account.delete()
  return Response('Account deleted successfully')  

################################################################################################################
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def posts(request):
  posts = Post.objects.all()
  serializers = PostSerializer(posts, many=True)
  return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_detail(request, id):
  post = Post.objects.get(id = id)
  serializers = PostSerializer(post, many=False)
  return Response(serializers.data)

@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def post_create(request):
  print(request.data)
  account = Account.objects.get(id = request.data["user_id"])
 

  serializers = CreatePostSerializer(data=request.data)
  
  # print(serializers)
  # Post.objects.create(user_id = account, description = request.data.get("description"), File = request.data.get("File"))
  try:
    print(serializers.is_valid())
    # serializers.save()
  except ValidationError as e:
    print(e)
  if serializers.is_valid():
    print("post valid")
    serializers.save()
  print(Response(serializers.data))
  # Post.objects.create(description=request.data.get("description"))


    
  # else:
  #   print(serializers.errors)
  return Response(serializers.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, id):
  post = Post.objects.get(id = id)
  Post.delete()
  return Response('Post deleted successfully')  

##############################################################################################################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def following(request, *args, **kwargs):
  token = Token.objects.get(key = kwargs.get("key"))
  account = Account.objects.get(user = token.user)
  following = Follow.objects.filter(follower = account)
  serializers = FollowSerializer(following, many=True)
  return Response(serializers.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request):
  serializers = NewFollowSerializer(data = request.data)
  if serializers.is_valid():
    serializers.save()
  

  return Response(serializers.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unfollow(request, followee, follower):
  follow = Follow.objects.get(followee = followee, follower = follower)
  follow.delete()
  return Response('Unfollowed successfully')

############################################################################################################################

@api_view(['GET'])
def likes(request):
  likes = Like.objects.all()
  serializers = LikeSerializer(likes, many=True)
  return Response(serializers.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request):
  serializers = LikeSerializer(data = request.data)
  if serializers.is_valid():
    serializers.save()
  return Response(serializers.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike(request, post_id, user_id, liked_by):
  like = Like.objects.get(post_id = post_id, user_id = user_id, liked_by = liked_by)
  like.delete()
  return Response('Unliked successfully')  

##########################################################################################################################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comments(request, id):
  # print(request._request)
  post = Post.objects.get(id = id)
  comments = Comment.objects.filter(post_id = post).order_by('-created_at')
  print(comments)
  serializers = CommentSerializer(comments, many=True)
  return Response(serializers.data)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def add_comment(request):
  # post = Post.objects.get(id = id)
  # comment = Comment.objects.filter(post_id = post)
  serializers = CommentSerializer(data = request.data)
  if serializers.is_valid():
    print("valid")
    serializers.save()
  return Response(serializers.data)

#############################################################################################################################
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
  response=""
  registration_serializers = RegistrationSerializer(data = request.data)
  if registration_serializers.is_valid():
    # if (registration_serializers.data.get("password1") == registration_serializers.data.get("password2")):
    #   try:
    #     User.objects.create(username = registration_serializers.data.get("username"), first_name = registration_serializers.data.get("first_name"), last_name = registration_serializers.data.get("last_name"), email = registration_serializers.data.get("email"), password = registration_serializers.data.get("password"))
    #   except:
    #     return Response("password didnt match")
    try:
      registration_serializers.save()
    except ValueError:
        return Response("Username already taken. Pickanother username")
    
    username = registration_serializers.data.get("username")
    password = registration_serializers.data.get("password")
    print(username, password)
    user = User.objects.get(username = username)
    auth_user = authenticate(username=username, password=password)
    print(auth_user)
    login(request,user)
    print(request.user)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "user": user.username, "image": str(token.user.account.profile_pic), 'userId': token.user.id, 'accountId': token.user.account.id, 'backgroundPic': str(token.user.account.background_pic) },  status=HTTP_200_OK)
  return Response("Registration failed")

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_view(request):
  username = request.data.get("username")
  password = request.data.get("password")
  print(username, password)
  if username is None or password is None:
    return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
  user = authenticate(username=username, password=password)
  if not user:
    return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
  token, _ = Token.objects.get_or_create(user=user)
  login(request,user)
  
  print(request.user)
  print(token.user.account)
  return Response({'token': token.key, 'user': token.user.username, 'name': token.user.account.full_name, 'email': token.user.account.email, 'image': str(token.user.account.profile_pic), 'userId': token.user.id, 'accountId': token.user.account.id, 'backgroundPic': str(token.user.account.background_pic) }, status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
  request.user.auth_token.delete()
  logout(request)
  return Response("Logged out succesfully")
