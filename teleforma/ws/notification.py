from teleforma.ws.logger import log_consumer_exceptions
from teleforma.models.notification import Notification
from django.conf import settings
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


@log_consumer_exceptions
class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()

        # send initial messages
        data = await self.get_notifications_list()
        await self.send_json(content={'type': 'initial', 'messages': data})

    @database_sync_to_async
    def get_notifications_list(self):
        messages = [message.to_dict() for message in Notification.objects.filter(
            user=self.user).order_by('-created')]
        return messages

    # Receive message from channel
    async def notification_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send_json(content={'type': 'new', 'messages': [message]})
