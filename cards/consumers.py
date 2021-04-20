import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Lobby, Card
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
class CardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("any attempt?")
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['lobby_id']
        print("ID>", self.id)
        self.room_group_name = 'lobby_%s' % self.id
        await self.channel_layer.group_add (
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard (
            self.room_group_name,
            self.channel_name
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)