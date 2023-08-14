from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    username = models.CharField(max_length=64)
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)
    mg = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} : {self.content}"