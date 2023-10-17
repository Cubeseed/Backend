from django.urls import path, re_path

# from . import consumers
from cubeseed.room.consumers import ChatConsumer
from cubeseed.room.consumers import NotificationConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter

websocket_urlpatterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
    path('ws/<str:room_name>/', ChatConsumer.as_asgi()),
]
