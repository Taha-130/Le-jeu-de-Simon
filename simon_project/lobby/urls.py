from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_game, name="create_game"),
    path("<str:code>/", views.room, name="room"),
    path("<str:code>/join/", views.join, name="join"),


]
