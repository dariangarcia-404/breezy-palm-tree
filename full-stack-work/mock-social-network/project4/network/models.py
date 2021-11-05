from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('User', related_name='followers', blank=True)
    user_likes = models.ManyToManyField('Post', related_name='likes', blank=True)


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_content = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)
