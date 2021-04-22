import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Lobby, Card
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from random import shuffle
# Players:
# Life Points, Deck reference, Cards in play, Cards in deck, Cards in discard, Cardss in hand
#
# Cards:
# Name, Health, Max Health, Attack, Defense, Level, Location


class CardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['lobby_id']
        self.lobby = await self.getLobby(self.id)
        ishost = await self.hostOrPlayer()
        istaken = await self.takenSlot()
        if ishost:
            self.scope['_host_deck'] = await self.querySetToList(self.user.decks.all())
            self.scope['_host_cards_in_deck'] = self.scope['_host_deck']
            self.scope['_player_deck'] = await self.querySetToList(self.lobby.player.decks.all())
            self.scope['_player_cards_in_deck'] = self.scope['_player_deck']
        elif istaken == False:
            self.scope['_host_deck'] = await self.querySetToList(self.lobby.host.decks.all())
            self.scope['_host_cards_in_deck'] = self.scope['_host_deck']
            self.scope['_player_deck'] = await self.querySetToList(self.user.decks.all())
            self.scope['_player_cards_in_deck'] = self.scope['_player_deck']
            await self.registerPlayer()
        self.scope['gameState'] = 1
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
                '_player_lp': self.scope['_player_lp'],
                'gameState': self.scope['gameState'],
                'initialization': True,
            }
        )
    @database_sync_to_async
    def getLobby(self, pk):
        return Lobby.objects.get(id=self.id)
    @database_sync_to_async
    def querySetToList(self, query_set):
        """
        Note that this function also shuffles the list
        """
        new_list = list()
        for i in query_set:
            new_card = {
                'attack': 0,
                'health': 0,
                'defense': 0,
                'card_art': 0,
                'effects': None,
                'level': 1,
            }
            new_card['name'] = i.name
            new_card['attack'] = i.attack
            new_card['health'] = i.health
            new_card['defense'] = i.defense
            new_card['card_art'] = i.card_art
            new_card['effects'] = i.effects
            new_card['level'] = i.level
            new_list.append(new_card)
        shuffle(new_list)
        return new_list
    @database_sync_to_async
    def hostOrPlayer(self):
        return self.lobby.host.id == self.user.id
    @database_sync_to_async
    def takenSlot(self):
        tPlayer = self.lobby.player
        if tPlayer: print(tPlayer.username, self.user.username)
        if tPlayer == None: return False
        if tPlayer.id == self.user.id: return False
        return True
    @database_sync_to_async
    def registerPlayer(self):
        L = self.lobby
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
        self.scope['gameState'] = text_data_json['gameState']
        # more information on these can be found in the file "acts.md"
        if text_data_json["action"] == "attack":
            if text_data_json['target'] == "host":
                self.scope['_host_lp'] = int(text_data_json['cur_value']) - int(text_data_json['value'])
                self.scope['_player_lp'] = int(text_data_json['my_lp'])
            elif text_data_json['target'] == "player":
                self.scope['_player_lp'] = int(text_data_json['cur_value']) - int(text_data_json['value'])
                self.scope['_host_lp'] = int(text_data_json['my_lp'])
            else:
                slot = int(text_data_json['target'])
                if slot <= 2:
                    self.scope['_host_cards_in_play'][slot]['health'] = (
                        int(text_data_json['cur_value']) - int(text_data_json['value'])
                    )
                    if self.scope['_host_cards_in_play'][slot]['health'] <= 0:
                        self.scope['_host_cards_in_play'][slot] = None
                else:
                    self.scope['_player_cards_in_play'][slot-3]['health'] = (
                        int(text_data_json['cur_value']) - int(text_data_json['value'])
                    )
                    if self.scope['_player_cards_in_play'][slot-3]['health'] <= 0:
                        self.scope['_player_cards_in_play'][slot-3] = None
        elif text_data_json['action'] == 'draw':
            if text_data_json['actor'] == 'host':
                i = int(text_data_json['value'])
                if self.scope['_host_cards_in_hand']:
                    self.scope['_host_cards_in_hand'] = list(self.scope['_host_cards_in_hand'])
                else:
                    self.scope['_host_cards_in_hand'] = list()
                while i > 0 and len(self.scope['_host_cards_in_deck']) > 0:
                    temp = self.scope['_host_cards_in_deck'].pop()
                    self.scope['_host_cards_in_hand'].append(temp)
                    i -= 1
            else:
                i = int(text_data_json['value'])
                if self.scope['_player_cards_in_hand']:
                    self.scope['_player_cards_in_hand'] = list(self.scope['_player_cards_in_hand'])
                else:
                    self.scope['_player_cards_in_hand'] = list()
                while i > 0 and len(self.scope['_player_cards_in_deck']) > 0:
                    temp = self.scope['_player_cards_in_deck'].pop()
                    self.scope['_player_cards_in_hand'].append(temp)
                    i -= 1
        elif text_data_json['action'] == 'playcard':
            if text_data_json['actor'] == 'host':
                i = int(text_data_json['position'])
                if not self.scope['_host_cards_in_play']: self.scope['_host_cards_in_play'] = list()
                self.scope['_host_cards_in_play'].append(self.scope['_host_cards_in_hand'].pop(i))
            else:
                i = int(text_data_json['position'])
                if not self.scope['_player_cards_in_play']: self.scope['_player_cards_in_play'] = list()
                self.scope['_player_cards_in_play'].append(self.scope['_player_cards_in_hand'].pop(i))
        await self.channel_layer.group_send (
            self.room_group_name,
            {
                'type': 'out',
                '_host_lp': self.scope['_host_lp'],
                '_host_deck': self.scope['_host_deck'],
                '_host_cards_in_play': self.scope['_host_cards_in_play'],
                '_host_cards_in_deck': self.scope['_host_cards_in_deck'],
                '_host_cards_in_discard': self.scope['_host_cards_in_discard'],
                '_host_cards_in_hand': self.scope['_host_cards_in_hand'],
                '_player_lp': self.scope['_player_lp'],
                '_player_deck': self.scope['_player_deck'],
                '_player_cards_in_play': self.scope['_player_cards_in_play'],
                '_player_cards_in_deck': self.scope['_player_cards_in_deck'],
                '_player_cards_in_discard': self.scope['_player_cards_in_discard'],
                '_player_cards_in_hand': self.scope['_player_cards_in_hand'],
                'gameState': self.scope['gameState'],
            }
        )