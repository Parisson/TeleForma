from teleforma.ws.logger import log_consumer_exceptions
from teleforma.models.core import Media, MediaRead
from django.conf import settings
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import json


@log_consumer_exceptions
class MediaReadConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        if self.scope["user"].is_anonymous:
            self.close()

        await self.accept()

        # send initial messages
        data = await self.get_duration(self.scope['user'])
        await self.send_json(content={'type': 'initial', 'messages': data})


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name 
        )

    @database_sync_to_async
    def get_duration(self, user, media):
        # import pdb;pdb.set_trace()
        if user.is_authenticated:
            duration, c = MediaRead.objects.get_or_create(
                user=user)
        else:
            duration = 0
        return duration

    # Receive message from channel
    async def notify(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send_json(content={'type': 'new', 'messages': [message]})
