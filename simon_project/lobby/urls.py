from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:code>/", views.room, name="room"),
    path("<str:code>/join/", views.join, name="join"),


]
