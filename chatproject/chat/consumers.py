import json
from random import randint
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from core.models import ChatRoom, Message, Notifications
connected_users = {}
class ChartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        for i in range(1000):
            await self.send(json.dumps({'value': randint(0, 200)}))
            await sleep(1)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        user_id = self.scope['user'].id
        connected_users[user_id] = self.channel_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        user_id = self.scope['user'].id
        del connected_users[user_id]
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        room = await self.get_room(self.room_id)
        saved_message = await self.save_message(room, user, message)
        await self.create_notification(room, user, message, saved_message)  # Create notification

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

    @database_sync_to_async
    def get_room(self, room_id):
        return ChatRoom.objects.get(id=room_id)

    @database_sync_to_async
    def save_message(self, room, user, message):
        return Message.objects.create(room=room, user=user, content=message)
    
    @database_sync_to_async
    def create_notification(self, room, user, message, saved_message):
        # Create a notification for each user in the room except the sender
        users_in_room = room.chatroomuser_set.exclude(user=user)
        for recipient in users_in_room:
            if recipient.user.id not in connected_users:
                Notifications.objects.create(room=room, user=recipient.user, sender=user, content=message, message=saved_message)
