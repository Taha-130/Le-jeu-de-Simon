from django.urls import path
from .consumers import SimonConsumer

websocket_urlpatterns = [
    path("ws/simon/", SimonConsumer.as_asgi()),
]