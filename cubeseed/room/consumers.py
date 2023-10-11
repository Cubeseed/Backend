import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User

from .models import Message, Room

from django.db.models import Q

from .serializer import MessageSerializer

# We need this when serializing UUID
# I believe something similar is required when
# serializing Date objects

# class UUIDEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, UUID):
#             # if the obj is uuid, we simply return the value of uuid
#             return obj.hex
#         return json.JSONEncoder.default(self, obj)

class ChatConsumer(AsyncWebsocketConsumer):

    # async def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.user = None
    #     self.room_name = None
    #     self.room = None

    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            print("not authenticated")
            return 
        
        # Use the following first line when connecting from a separate frontend
        # but when testing with a backend rendered template uncomment and use the
        # second line, comment out the first line
        self.room_name = await self.get_or_create_room(self.scope['url_route']['kwargs']['room_name'], self.scope['user'])
        print("Printing room name: ", self.room_name)
        # self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        room = data['room']

        # self.room_name represents to_user
        saved_message = await self.save_message(
            from_user=self.user.username, 
            to_user=self.scope['url_route']['kwargs']['room_name'],
            room=room,
            content=message
        )
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                # 'message': MessageSerializer(saved_message, context={'request': self.scope['request']}).data,
                # 'message': MessageSerializer(saved_message).data,
                'message': saved_message.content,
                'from_user': {'username': self.user.username},
                'room': room
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # username = event['username']
        from_user= event['from_user']
        room = event['room']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            # 'username': username,
            'from_user': from_user,
            'room': room,
        }))
    
    @sync_to_async
    # def save_message(self, username, room, message):
    def save_message(self, from_user, to_user, room, content):
        from_user = User.objects.get(username=from_user)
        to_user = User.objects.get(username=to_user)
        room = Room.objects.get(slug=self.room_name)

        saved_message = Message.objects.create(
            room=room,
            from_user=from_user, 
            to_user=to_user, 
            content=content
        )
        return saved_message
    
    @sync_to_async
    def get_or_create_room(self, room, username):
        # Get the room_name if it exists otherwise create it
        room_name = "{}-{}".format(room, username)
        reverse_room_name = "{}-{}".format(username, room)

        # Create the Room if it does not exist
        if not Room.objects.filter(Q(slug=room_name) | Q(slug=reverse_room_name)).exists():
            Room.objects.create(slug=room_name, name=room_name)
        
        room = Room.objects.get(Q(slug=room_name) | Q(slug=reverse_room_name))
        return room.slug

    # @classmethod
    # def encode_json(cls, content):
    #     return json.dumps(content, cls=UUIDEncoder)