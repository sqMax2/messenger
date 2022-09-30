"""
WebSocket consumer
"""

import json
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # print(await sync_to_async(User.objects.get)(id=self.user.id))
        try:
            if await sync_to_async(User.objects.get)(id=self.user.id):
                await self.send(text_data=json.dumps({
                    'message': '',
                    'auth': 'auth',
                    'username': self.user.username,
                }))
        except:
            await self.send(text_data=json.dumps({
                'message': '',
                'auth': 'anon',
                'username': self.user.username,
            }))
            return AnonymousUser()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        # check for sending to OTHERS
        if (username != self.user.username)|True:
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
            }))
