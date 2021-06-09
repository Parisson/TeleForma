# chat/consumers.py
from teleforma.ws.logger import log_consumer_exceptions
from teleforma.models.chat import ChatMessage
from django.conf import settings 
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async




@log_consumer_exceptions
class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        # self.redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0,
        #             ssl=True, ssl_cert_reqs=None)
        # self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)
        print('join room')

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # import pdb;pdb.set_trace()
        # self.pubsub.subscribe([self.room_group_name, ])

        print(self.room_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        

        # self.redis.subscribe(self.room_group_name)
        print("group added")

        await self.accept()
        print('accepted')

        print("listen")
        # for message in self.pubsub.listen():
        #     print("listen ok")
        #     print(message)
        print("end of listen")
        

    async def disconnect(self, close_code):
        print('disconnect')
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
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
        print(event)
        print("TEST TEST TEST")
        message = event['message']

        print("send to socket", message)
        # Send message to WebSocket
        await self.send_json(content=message)