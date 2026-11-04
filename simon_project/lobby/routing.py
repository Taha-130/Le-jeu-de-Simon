from django.urls import re_path
from .consumers import SimonConsumer

websocket_urlpatterns = [
    re_path(r"^ws/simon/(?P<code>[A-Z0-9]{6})/$", SimonConsumer.as_asgi()),
]