import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User , Post
from .forms import UserForm , PostForm

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

        user = User.objects.get(pk= id_user)
        posts_user = Post.objects.filter(id_user=user.id)
        posts_order = sorted(posts_user, key=lambda x: x.date, reverse=True)
        return render(request, 'network/individualprofile.html', {
            "userindividual": user,
            "posts" : posts_order
        })

    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data["state"] )
        print(" LLEGAMOS DENTRO DE LA VISTAAAAAAAAAA ")
        print(id_user)
        print(request.user.id)       
        # obtenemos el usuario que a sido seguido
        usuario_seguido = User.objects.get(pk=id_user)
        # y el que siguio
        usuario_seguidor = User.objects.get(pk=request.user.id)

        #nos fijamos si el usuario ya lo sigue o no
        if data["state"] == "Follow":
            response_data = {"content": "Following"}
            return JsonResponse(response_data)
        else:
            response_data = {"content": "Follow"}
            return JsonResponse(response_data)
           


    else:
        # Si se realiza una solicitud que no sea GET ni PUT, devuelve un error
        return JsonResponse({"error": "GET or PUT request required."}, status=400)



    


