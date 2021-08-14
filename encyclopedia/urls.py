from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("random", views.random, name="random"),
    path("new", views.create, name="new"),
    path("edit/<str:entry_name>", views.edit, name="edit"),
    path("search", views.search, name='search')
]
