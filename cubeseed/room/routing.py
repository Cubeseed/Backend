"""Room Websocket Routing"""
from django.urls import path, re_path

# from . import consumers
from cubeseed.room.consumers import ChatConsumer
from cubeseed.room.consumers import NotificationConsumer, ConversationNotificationConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter

websocket_urlpatterns = [
    path('ws/notifications/<str:other_user>/', ConversationNotificationConsumer.as_asgi()),
    path('ws/notifications/', NotificationConsumer.as_asgi()),
    path('ws/<str:room_name>/', ChatConsumer.as_asgi()),
]
