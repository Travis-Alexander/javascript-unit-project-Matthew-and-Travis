import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Message, Room
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        #only a place holder