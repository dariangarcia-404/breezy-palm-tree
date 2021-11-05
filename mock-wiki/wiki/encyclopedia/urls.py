from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.subject, name="subject"),
    path("search", views.searchpage, name="searchpage"),
    path("edit", views.editpage, name="editpage"),
    path("new", views.newpage, name="newpage"),
    path("randompage", views.randompage, name="randompage")
]
