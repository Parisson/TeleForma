import os, sys
from django.core.asgi import get_asgi_application

#sys.path.append(os.path.dirname('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from teleforma.ws import chat

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', chat.ChatConsumer.as_asgi()),
    re_path(r'ws/notification/(?P<user_id>\w+)/$', notification.NotificationConsumer.as_asgi()),
]


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
