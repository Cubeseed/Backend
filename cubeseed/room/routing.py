from django.urls import path, re_path

from . import consumers
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    # re_path(r'^/ws/hobby/', consumers.ChatConsumer.as_asgi()),
]


# from channels.routing import ProtocolTypeRouter, URLRouter
# application = ProtocolTypeRouter({
#     # 'websocket': AuthMiddlewareStack(
#        'websocket': URLRouter([
#             path('ws/work/', consumers.ChatConsumer.as_asgi()),
#         ])
#     # )
# })