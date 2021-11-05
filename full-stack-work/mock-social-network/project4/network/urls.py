
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/<str:title>", views.index, name="posts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createpost", views.createpost, name="createpost"),
    path("posts/<int:post_id>/edit", views.edit, name="edit"),
    path("posts/<int:post_id>/like", views.like, name="like"),
    path("posts/<int:post_id>/unlike", views.unlike, name="unlike"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
]
