from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name='following', blank=True)
    following = models.ManyToManyField('self', related_name='followers', blank=True)

class Post(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)
    mg = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} : {self.content}"