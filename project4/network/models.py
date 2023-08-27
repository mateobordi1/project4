from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)
    mg = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} : {self.content}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} follows {self.following}'