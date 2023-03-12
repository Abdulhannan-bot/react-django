from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
  path('', apiOverview, name='api'),
  path('api-token-auth/', obtain_auth_token, name='obtain_auth_token'),
  ##########################################################################
  path('accounts', accounts, name='accounts'),
  path('account-detail/<str:key>', account_detail, name='account_detail'),
  path('account-create', account_create, name='account_create'),
  path('account-update/<str:id>', account_update, name='account_update'),
  path('account-delete/<str:id>', account_delete, name='account_delete'),
  path('account-info/<str:id>/<str:key>', account_info, name='account_info'),
  ##########################################################################
  path('posts', posts, name='posts'),
  path('post-create', post_create, name='post_create'),
  path('post-delete', post_delete, name='post_delete'),
  ##########################################################################
  path('following/<str:key>', following, name='follows'),
  path('follow', follow, name='follow'),
  path('unfollow/<int:followee>/<int:follower>', unfollow, name='unfollow'),
  ##########################################################################
  path('lilkes', likes, name='likes'),
  path('like', like, name='like'),
  path('unlike/<int:post_id>/<int:user_id>/<int:liked_by>', unlike, name='unlike'),
  ##########################################################################
  path('comments/<str:id>', comments, name='comments'),
  path('add-comment', add_comment, name='add_comment'),
  ##########################################################################
  path('register', register ,name='register'),
  path('login', login_view, name='login'),
  path('logout', logout_view, name='logout'),
]