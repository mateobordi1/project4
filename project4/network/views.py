import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User , Post, Follow
from .forms import UserForm , PostForm, FollowForm

def index(request):
    posts = Post.objects.all()
    posts_order = sorted(posts, key=lambda x: x.date, reverse=True)
    return render(request, "network/index.html", {
        "posts": posts_order
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():         
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse(form.errors)

    else:
        return render(request, 'network/newpost.html')

def individualprofile(request, id_user):

    if request.method == "GET":

        user_profile = User.objects.get(pk= id_user)
        user_logued = User.objects.get(pk=request.user.id)

        posts_user = Post.objects.filter(id_user=user_profile.id)
        posts_order = sorted(posts_user, key=lambda x: x.date, reverse=True)
        
    
        follower = Follow.objects.filter(follower=user_logued , following= user_profile)
        if len(follower) != 0 :
            state_follow = True
        else: 
            state_follow= False


        followers = user_profile.followers.count()
        following = user_profile.following.count()
        return render(request, 'network/individualprofile.html', {
            "userindividual": user_profile,
            "posts" : posts_order,
            "followers" : followers,
            "following" : following,
            "state" : state_follow
        })

def follow(request):
    if request.method == "POST":
        form = FollowForm(request.POST)
        if form.is_valid():
            form.save()
            follower_id = form.cleaned_data['follower']
            return HttpResponseRedirect(reverse('individualprofile', args=[follower_id.id]))
    else:
        return HttpResponse("Se requiere el metodo post")

def unfollow(request):
    if request.method == "POST":
        form = FollowForm(request.POST)
        if form.is_valid():
            follower_id = form.cleaned_data['follower']
            following_id = form.cleaned_data['following']
            follow_to_delete = Follow.objects.filter(follower=follower_id , following=following_id)
            follow_to_delete.delete()
            return HttpResponseRedirect(reverse('individualprofile', args=[follower_id.id]))
    else:
        return HttpResponse("Se requiere el metodo post")

def post_following(request):
    if request.method == "GET":
        user_logued = User.objects.get(pk=request.user.id)
        users_following = Follow.objects.filter(follower=user_logued)

        user_ids_following = [user_following.following.id for user_following in users_following]
        
        posts = Post.objects.filter(id_user__in=user_ids_following)
        posts_order = sorted(posts, key=lambda x: x.date, reverse=True)
        return render(request , 'network/postfollowing.html', {
            "users": users_following , 
            "posts": posts_order
        })
    


