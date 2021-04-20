from django.urls import re_path
from .consumers import CardConsumer
websocket_urlpatterns = [
    re_path(r"ws/lobby/(?P<lobby_id>\d+)/$", CardConsumer.as_asgi()),
]