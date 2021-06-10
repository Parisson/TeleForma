# chat/consumers.py
from teleforma.ws.logger import log_consumer_exceptions
from teleforma.models.chat import ChatMessage
from django.conf import settings 
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

@log_consumer_exceptions
class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('join room')

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from cha
    async def receive_json(self, content):
        message_content = content['message'][:255]

        message = await self.add_message_to_db(self.scope['user'], self.room_name, message_content)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        

    @database_sync_to_async
    def add_message_to_db(self, user, room_name, message):
        return ChatMessage.add_message(user, room_name, message)
        
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send_json(content=message)