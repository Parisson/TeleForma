from teleforma.ws.logger import log_consumer_exceptions
from teleforma.models.notification import Notification
from django.conf import settings
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import json

@log_consumer_exceptions
class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        if self.scope["user"].is_anonymous:
            self.close()

        await self.accept()

        self.room_group_name = f"notifications_{self.scope['user'].id}"
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # send initial messages
        data = await self.get_notifications_list(self.scope['user'])
        await self.send_json(content={'type': 'initial', 'messages': data})


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name 
        )

    @database_sync_to_async
    def get_notifications_list(self, user):
        # import pdb;pdb.set_trace()
        if user.is_authenticated:
            messages = [message.to_dict() for message in Notification.objects.filter(
                user=user).order_by('-created')][:50]
        else:
            messages = []
        return messages

    # Receive message from channel
    async def notify(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send_json(content={'type': 'new', 'messages': [message]})
