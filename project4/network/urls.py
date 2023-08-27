
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="new_post"),
    path("user/<int:id_user>", views.individualprofile , name="individualprofile" ),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("post_following" , views.post_following, name="postfollowing")
]
