from django.urls import re_path
from .consumers import GameConsumer
websocket_urlpatterns = [
    re_path(r"ws/chat/room/(?P<room_id>\d+)/$", GameConsumer.as_asgi()),
]