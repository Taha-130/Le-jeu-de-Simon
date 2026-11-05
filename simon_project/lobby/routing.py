from django.urls import path
from .consumers import SimonConsumer

websocket_urlpatterns = [
    path("ws/simon/<str:code>/", SimonConsumer.as_asgi()),
]