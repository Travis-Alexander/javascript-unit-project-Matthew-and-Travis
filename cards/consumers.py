import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Lobby, Card
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

# Players:
# Life Points, Deck reference, Cards in play, Cards in deck, Cards in discard, Cardss in hand
#
# Cards:
# Name, Health, Max Health, Attack, Defense, Level, Location


class CardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['lobby_id']
        ishost = await self.hostOrPlayer()
        print(ishost)
        istaken = await self.takenSlot()
        if ishost:
            self.scope['_host_deck'] = self.user.decks
            self.scope['_host_cards_in_deck'] = self.scope['_host_deck']
        elif istaken == False:
            self.scope['_player_deck'] = self.user.decks
            self.scope['_player_cards_in_deck'] = self.scope['_player_deck']
            await self.registerPlayer()
        
        self.scope['_host_lp'] = 2000
            
        self.scope['_host_cards_in_play'] = None
            
        self.scope['_host_cards_in_discard'] = None
        self.scope['_host_cards_in_hand'] = None
        
        self.scope['_player_lp'] = 2000
        self.scope['_player_cards_in_play'] = None
        self.scope['_player_cards_in_discard'] = None
        self.scope['_player_cards_in_hand'] = None
        self.room_group_name = 'lobby_%s' % self.id
        await self.channel_layer.group_add (
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        await self.channel_layer.group_send (
            self.room_group_name,
            {
                'type': 'out',
                '_host_lp': self.scope['_host_lp'],
            }
        )
    @database_sync_to_async
    def hostOrPlayer(self):
        return Lobby.objects.get(id=self.id).host.id == self.user.id
    @database_sync_to_async
    def takenSlot(self):
        tPlayer = Lobby.objects.get(id=self.id).player
        if tPlayer: print(tPlayer.username, self.user.username)
        if tPlayer == None: return False
        if tPlayer.id == self.user.id: return False
        return True
    @database_sync_to_async
    def registerPlayer(self):
        L = Lobby.objects.get(id=self.id)
        L.player = self.user
        L.save()
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard (
            self.room_group_name,
            self.channel_name
        )
    async def out(self, event):
        await self.send(text_data=json.dumps(event))
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send (
            self.room_group_name,
            {
                'type': 'out',
                '_host_lp': self.scope['_host_lp'],
                '_host_deck': self.scope['_host_deck'],
                '_host_cards_in_play': self.scope['_host_cards_in_play'],
                '_host_cards_in_deck': self.scope['_host_cards_in_play'],
                '_host_cards_in_discard': self.scope['_host_cards_in_play'],
                '_host_cards_in_hand': self.scope['_host_cards_in_play'],
            }
        )