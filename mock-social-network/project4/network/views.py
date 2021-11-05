from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post
import json


def index(request, title="all"):
    return showposts(title, request)


def showposts(title, request):
    profile_user = None
    if title == "all":
        posts = Post.objects.all()
    elif title == "following":
        if request.user.is_authenticated:
            user = request.user
            posts = Post.objects.filter(poster__in=user.following.all()).order_by("-time_stamp").all()
        else:
            return render(request, 'network/error.html', {
                'message': "you're not a user."
            })
    else:  # title == <username> for profile view
        profile_user = User.objects.get(username=title)
        posts = Post.objects.filter(
                poster=profile_user).order_by("-time_stamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {
        'page': page_obj,
        "title": title,
        "profile_user": profile_user,
        "following": request.user.following.all()
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


@login_required
def edit(request, post_id):
    if request.method == "PUT":
        # see if post exists
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        # only allow poster to edit, if not poster give 403
        if request.user != post.poster:
            return JsonResponse(
                {"error": "Not your post, can't edit."},
                status=403)
        # convert request using json.loads get content
        # set post content to that content.
        data = json.loads(request.body)
        post.post_content = data["content"]
        post.save()
        # return
        return JsonResponse({
            "id": post_id,
            "content": post.content,
            "likes": post.likes.count()
        })


@login_required
def createpost(request):
    message = ""
    if request.method == "POST":
        poster = request.user
        post_content = request.POST["post_content"]
        post = Post(poster=poster, post_content=post_content)
        post.save()
        message = "Post was created"
    return showposts("all", request)


@login_required
def follow(request, username):
    if request.method == "POST":
        try:
            profile_user = User.objects.get(username=username)
            current_user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            raise Http404("User does not exist.")
        if profile_user != current_user:
            current_user.following.add(profile_user)
            current_user.save()
    return showposts(username, request)


@login_required
def unfollow(request, username):
    if request.method == "POST":
        try:
            profile_user = User.objects.get(username=username)
            current_user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            raise Http404("User does not exist.")
        if profile_user != current_user:
            current_user.following.remove(profile_user)
            current_user.save()
    return showposts(username, request)


@login_required
def like(request, post_id):
    pass


@login_required
def unlike(request, post_id):
    pass
