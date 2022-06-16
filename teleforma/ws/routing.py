import os, sys
from channels.auth import AuthMiddlewareStack

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from . import chat
from . import notification

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teleforma.settings')
sys.path.append(os.path.dirname('.'))


websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', chat.ChatConsumer.as_asgi()),
    re_path(r'ws/notification/(?P<user_id>\w+)/$', notification.NotificationConsumer.as_asgi()),
]


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})





