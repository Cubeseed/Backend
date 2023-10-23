import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync

from django.contrib.auth.models import User

from .models import Message, Room

from django.db.models import Q

from .serializer import MessageSerializer

import datetime

from channels.db import database_sync_to_async


def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            print("not authenticated")
            return 
        
        self.both_users_joined_room_name = await self.get_or_create_room(self.scope['url_route']['kwargs']['room_name'], self.scope['user'])

        self.room_group_name = 'chat_%s' % self.both_users_joined_room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        online_users = await sync_to_async(list)(self.room.online.all())

        await self.send(text_data=json.dumps({
            "type": "online_user_list",
            "users": [user.username for user in online_users],
        }))

        await self.channel_layer.group_send(
            self.room_group_name,
                {
                    "type": "user_join",
                    "user": self.user.username,
                },
            )

        await sync_to_async(self.room.online.add)(self.user)



    async def disconnect(self, code):

        if self.user.is_authenticated: 
            # send the leave event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                    {
                        "type": "user_leave",
                        "user": self.user.username,
                    },
            )
            await sync_to_async(self.room.online.remove)(self.user)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        return super().disconnect(code)


    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        if (data.get('message')):
            message = data['message']
        if (data.get('room')):
            room = data['room']
        if (data.get('type')):
            type = data['type']

        if type == "read_messages":
            print("In here")
            messages_to_me = await sync_to_async(self.room.messages.filter)(to_user=self.user)
            await sync_to_async(messages_to_me.update)(read=True)
        
            # Update the unread message count
            unread_count = await sync_to_async(Message.objects.filter(to_user=self.user, read=False).count)()
            print("unread count: ", unread_count)
            await self.channel_layer.group_send(
                self.user.username + "__notifications",
                {
                    "type": "unread_count",
                    "unread_count": unread_count,
                },
            )

        else:
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
                    'message': saved_message.content,
                    'date_added': json.dumps(saved_message.date_added, default=serialize_datetime),
                    'from_user': {'username': self.user.username},
                    'room': room
                }
            )

            notification_group_name = self.scope['url_route']['kwargs']['room_name'] + "__notifications"
            await self.channel_layer.group_send(
                notification_group_name,
                {
                    "type": "new_message_notification",
                    "name": self.user.username,
                },
            )

    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        from_user= event['from_user']
        room = event['room']
        date_added = event['date_added']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'from_user': from_user,
            'room': room,
            'date_added': date_added
        }))
    
    @sync_to_async
    def save_message(self, from_user, to_user, room, content):
        from_user = User.objects.get(username=from_user)
        to_user = User.objects.get(username=to_user)
        room = Room.objects.get(slug=self.both_users_joined_room_name)

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
        # Saving the room in self
        self.room = room
        return room.slug

    async def user_join(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing(self, event):
        await self.send(text_data=json.dumps(event))

    async def new_message_notification(self, event):
        await self.send(text_data=json.dumps(event))

    async def unread_count(self, event):
        await self.send(text_data=json.dumps(event))



class NotificationConsumer(AsyncWebsocketConsumer):
 
    async def connect(self):
        # The line below must be added to init
        self.notification_group_name = None

        self.user = self.scope.get("user")
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        await self.accept()

        # private notification group
        self.notification_group_name = self.user.username + "__notifications"
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name,
        )
        
        unread_count = await sync_to_async(Message.objects.filter(to_user=self.user, read=False).count)()
        await self.send(text_data=json.dumps({
            "type": "unread_count",
            "unread_count": unread_count,   
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name,
        )
        return super().disconnect(code)
    
    async def new_message_notification(self, event):
        await self.send(text_data=json.dumps(event))

    async def unread_count(self, event):
        await self.send(text_data=json.dumps(event))