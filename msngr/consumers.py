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

from msngr.models import Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
        self.user_inbox = f'inbox_{self.user.username}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        try:
            if await sync_to_async(User.objects.get)(id=self.user.id):
                await self.send(text_data=json.dumps({
                    'type': 'auth',
                    'message': '',
                    'auth': 'auth',
                    'username': self.user.username,
                }))
                await self.channel_layer.group_add(
                    self.user_inbox,
                    self.channel_name,
                )
                # await self.channel_layer.group_send(
                #     self.room_group_name,
                #     {
                #         'type': 'join',
                #         'message': '',
                #         'username': self.user.username,
                #     }
                # )
        except:
            await self.send(text_data=json.dumps({
                'type': 'auth',
                'message': '',
                'auth': 'anon',
                'username': self.user.username,
            }))
            return AnonymousUser()


    async def disconnect(self, close_code):
        # Leave room group
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.user_inbox,
            self.channel_name,
        )
        try:
            room_object = await sync_to_async(Room.objects.get)(name=self.room_name)
        except:
            pass
        else:
            await sync_to_async(room_object.leave)(self.user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'leave',
                'message': '',
                'username': self.user.username,
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        mtype = text_data_json['type']
        if mtype == 'delete.room':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete.room',
                    'message': message,
                    'username': username,
                }
            )
        elif mtype == 'join' or mtype == 'leave':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': mtype,
                    'message': message,
                    'username': username,
                }
            )
        # private messaging
        elif message.startswith('/pm '):
            split = message.split(' ', 2)
            target = split[1]
            target_msg = split[2]

            # send private message to the target
            await self.channel_layer.group_send(
                f'inbox_{target}',
                {
                    'type': 'private_message',
                    'user': self.user.username,
                    'message': target_msg,
                }
            )
            # send private message delivered to the user
            await self.send(json.dumps({
                'type': 'private_message_delivered',
                'target': target,
                'message': target_msg,
            }))
            return

        else:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'username': username,
                }
            )

    async def delete_room(self, event):
        # Leave room and delete
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'deletion',
                'message': 'deletes room. Bye',
                'username': event['username'],
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # room_object = await sync_to_async(Room.objects.get)(name=self.room_name)
        # await sync_to_async(room_object.delete)()

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        mtype = event['type']

        # Send message to WebSocket
        # check for sending to OTHERS
        if (username != self.user.username) | True:
            await self.send(text_data=json.dumps({
                'type': mtype,
                'message': message,
                'username': username,
            }))

    async def join(self, event):
        username = event['username']
        mtype = event['type']
        if (username != self.user.username) | True:
            await self.send(text_data=json.dumps({
                'type': mtype,
                'message': '',
                'username': username,
            }))

    async def leave(self, event):
        username = event['username']
        mtype = event['type']
        if (username != self.user.username) | True:
            await self.send(text_data=json.dumps({
                'type': mtype,
                'message': '',
                'username': username,
            }))

    async def private_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def private_message_delivered(self, event):
        await self.send(text_data=json.dumps(event))

    async def deletion(self, event):
        await self.send(text_data=json.dumps(event))
