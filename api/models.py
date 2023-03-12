from django.db import models

# Create your models here.

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Account(models.Model):
  user = models.OneToOneField(User, null = True, on_delete = models.CASCADE)
  email = models.EmailField(max_length = 224, null = True, blank = True)
  full_name = models.CharField(max_length = 100, null = True, blank = True)
  created_at = models.DateTimeField(auto_now_add = True, null = True)
  profile_pic = models.ImageField(default="house1.png", null = True, blank = True)
  background_pic = models.ImageField(default="cover-photo_hVs4cgX_G9aAZgR.png", null = True, blank = True)

  def __str__(self):
    return str(self.user)

class Post(models.Model):
  description = models.TextField(null = True, blank = True)
  File = models.FileField(null = True, blank = True)
  user_id = models.ForeignKey(Account, null = True, blank=True, on_delete=models.SET_NULL)
  # user_name = models.CharField(max_length = 100, null = True, blank = True)
  # profile = models.ImageField(null = True, blank = True)
  created_at = models.DateTimeField(auto_now_add = True, null = True)


class Follow(models.Model):
  follower = models.ForeignKey(Account, related_name="follower", on_delete=models.CASCADE)
  followee = models.ForeignKey(Account, related_name="followee", on_delete=models.CASCADE)
  # follow_helper = str(follower)+ "followes" + str(followee)

class Comment(models.Model):
  text = models.TextField(null = True)
  post_id = models.ForeignKey(Post, null = True, blank = True, on_delete=models.SET_NULL)
  user_id = models.ForeignKey(Account, null = True, blank = True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add = True, null = True)


  def __str__(self):
    return str(self.text[:10])+"....."

class Like(models.Model):
  user_id = models.ForeignKey(Account, null = True, blank = False, on_delete=models.SET_NULL, related_name="post_by")
  post_id = models.ForeignKey(Post, null = True, blank = False, on_delete=models.SET_NULL)
  liked_by = models.ForeignKey(Account, null = True, blank = False, on_delete=models.SET_NULL, )

  def __str__(self):
    return str(self.liked_by) + " likes a post by " + str(self.user_id)


class Node(object):
  def __init__(self, account):
    self.account = account
    self.link = []

class Edge(object):
  def __init__(self,account_from,account_to):
    self.account_from = account_from
    self.account_to = account_to


class Connection(object):
  def __init__(self, accounts = [], follows = []):
    self.accounts = accounts
    self.follows = follows

  def create_follow(self, account_from, account_to):
    from_found = None
    to_found = None

    for account in self.accounts:
      if account_from == account:
        from_found = account
      if account_to == account:
        to_found = account

    if from_found == None:
      from_found = Node(account_from)
      self.accounts.append(from_found)
    if to_found == None:
      to_found = Node(account_to)
      self.accounts.append(to_found)

    new_edge = Edge(from_found, to_found)
    from_found.link.append(new_edge)
    to_found.link.append(new_edge)
    self.follows.append(new_edge) 

  def get_connection_list(self):
    connection_list = []
    for follow in self.follows:
        connection_list.append((follow.account_from.account, follow.account_to.account))
    return connection_list


connect = Connection()

@receiver(post_save, sender = User)
def user_generator(sender, created, instance, **kwargs):
  if created:
    Token.objects.create(user=instance)
    Account.objects.create(
      user = instance,
      email = instance.email,
      full_name = instance.first_name+" "+instance.last_name
    )

@receiver(post_save, sender = Follow)
def make_connection(sender, created, instance, **kwargs):
  if created:
    connect.create_follow(instance.follower, instance.followee)
    print(connect.get_connection_list())
