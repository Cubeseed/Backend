"""Room Consumers"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from .models import Message, Room
from django.db.models import Q
from .serializer import MessageSerializer
import datetime
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
import environ
from django.conf import settings
from rest_framework import serializers

env = environ.Env()
env.read_env()

User = get_user_model()

def serialize_datetime(obj):
    """
    datetime serializer, converts a datetime.datetime 
    object to its string representation in the ISO 8601 
    format

    Parameters:
    obj: datetime.datetime

    Returns:
    String
        Returns the string representation of the datetime 
        object in the ISO 8601 format.
    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        Handles new WebSocket connection. Authenticates user, joins them 
        to a chat room, sends online users list, and notifies the room of 
        their arrival.
        """
        self.user = self.scope["user"]

        # Checking if user is authenticated
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        
        # Retrieving or creating a chat room based on the username of the authenticated user 
        # and the room name provided in the URL route.
        self.both_users_joined_room_name = await self.get_or_create_room(self.scope['url_route']['kwargs']['room_name'], self.scope['user'])

        self.room_group_name = 'chat_%s' % self.both_users_joined_room_name

        # Adding the current channel to a group named after the chat room.
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accepting the WebSocket connection.
        await self.accept()

        # Retrieving a list of online users in the room
        online_users = await sync_to_async(list)(self.room.online.all())

        # Sending the list of online users to the client
        await self.send(text_data=json.dumps({
            "type": "online_user_list",
            "users": [user.username for user in online_users],
        }))

        # Sending a message to the group indicating that a new user has joined.
        await self.channel_layer.group_send(
            self.room_group_name,
                {
                    "type": "user_join",
                    "user": self.user.username,
                },
            )
        
        # Adding the user to the list of online users in the room.
        await sync_to_async(self.room.online.add)(self.user)



    async def disconnect(self, code):
        """
        Handles websocket disconnection. Notifies the room of the user's
        departure, removes user from the list of online users in the 
        room, removes the channel from the group, and calls the superclass's
        disconnect method, finalizing the disconnection process.

        Parameters:
        code: Integer
            Represents the WebSocket close code, indicating the reason for 
            closing the WebSocket connection
        """

        if self.user.is_authenticated: 
            # send the leave event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                    {
                        "type": "user_leave",
                        "user": self.user.username,
                    },
            )
            # remove user from the list of online users in the room
            await sync_to_async(self.room.online.remove)(self.user)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Calling the superclass's disconnect method
        # which finalizes the disconnection process.
        return super().disconnect(code)


    # Receive message from WebSocket
    async def receive(self, text_data):
        """
        Handles receiving the events from the WebSocket, it
        handles two types of events, 'read_messages' and 'chat_message'.
        The 'read_messages' event is sent when the user reads the messages
        in the chat room. The 'chat_message' event is sent when the user
        sends a message to the chat room.

        Parameters:
        text_data: String
            A string representing the data sent by the client

        Returns:
            Does not return anything
        """
        data = json.loads(text_data)
        if (data.get('message')):
            message = data['message']
        if (data.get('room')):
            room = data['room']
        if (data.get('type')):
            type = data['type']

        if type == "read_messages":
            # Marking all the messages in the room that are
            # sent to the authenticated user as read
            messages_to_me = await sync_to_async(self.room.messages.filter)(to_user=self.user)
            await sync_to_async(messages_to_me.update)(read=True)
        
            # Get the total number of unread messages the authenticated user has
            # Message notification group
            unread_count = await sync_to_async(Message.objects.filter(to_user=self.user, read=False).count)()
            await self.channel_layer.group_send(
                self.user.username + "__notifications",
                {
                    "type": "unread_count",
                    "unread_count": unread_count,
                },
            )
            # Get all the unread messages a user has from a particular user 
            # (the other user in the conversation/room)
            # Message the per conversation notification group
            self.from_user = self.scope['url_route']['kwargs']['room_name']
            # Getting the user model
            from_user_model = await sync_to_async(get_user_model().objects.get)(username=self.from_user)
            unread_count = await sync_to_async(Message.objects.filter(to_user=self.user, from_user=from_user_model, read=False).count)()
            await self.channel_layer.group_send(
                self.from_user + self.user.username + "__conversation_notifications",
                {
                    "type": "single_conversation_unread_count",
                    "unread_count": unread_count,
                },
            )

        if type == "chat_message":
            # If the multimedia_url does not exist None will be saved
            # to the database, since the multimedia_url field is nullable

            # In the case were the multimedia_url, their are two possibilities
            # 1. The server is running in production mode and the multimedia_url is an s3 link
            # 2. The server is running in development mode and the multimedia_url is a local link
            if data.get('multimedia_url') is not None and settings.DEBUG==False:
                # This indicates that the server is running in production mode
                # and the multimedia_url is an s3 link
                multimedia_save_location='s3'
            elif data.get('multimedia_url') is not None and settings.DEBUG==True:
                # This indicates that the server is running in development mode
                # and the multimedia_url is a local link
                multimedia_save_location='local'
            else:
                multimedia_save_location=None

            # Saving the message to the database
            saved_message = await self.save_message(
                from_user=self.user.username, 
                to_user=self.scope['url_route']['kwargs']['room_name'],
                content=message,
                multimedia_url=data.get('multimedia_url'),
                multimedia_save_location=multimedia_save_location,
                file_identifier=data.get('file_identifier'),
                multimedia_url_expiration=data.get('multimedia_url_expiration')
            )

            # If the multimedia_url is save locally, a working link must be generated 
            if saved_message.multimedia_url and saved_message.multimedia_save_location == 'local':
                # This working link will be sent to the group
                multimedia_url = generate_working_link_for_local_multimedia(saved_message.multimedia_url)
            else:
                # It is an s3 link or there is no multimedia, generation of
                # a working link is not required
                multimedia_url = saved_message.multimedia_url
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'id': saved_message.id,
                    'message': saved_message.content,
                    'multimedia_url': multimedia_url,
                    'date_added': json.dumps(saved_message.date_added, default=serialize_datetime),
                    'from_user': {'username': self.user.username},
                }
            )

            # Send a new message notification to the notification group
            notification_group_name = self.scope['url_route']['kwargs']['room_name'] + "__notifications"
            await self.channel_layer.group_send(
                notification_group_name,
                {
                    "type": "new_message_notification",
                },
            )

            # Send a new message notification to the per conversation notification group
            single_conversation_notification_group_name = self.user.username + saved_message.to_user.username + "__conversation_notifications"
            await self.channel_layer.group_send(
                single_conversation_notification_group_name,
                {
                    "type": "single_conversation_new_message_notification",
                },
            )

            await self.channel_layer.group_send(
                single_conversation_notification_group_name,
                {
                    "type": "single_conversation_last_message",
                    "last_message": saved_message.content,
                    "last_datetime": json.dumps(saved_message.date_added, default=serialize_datetime)
                }
            )


    @sync_to_async
    def save_message(self, from_user, to_user, content, multimedia_url, multimedia_save_location, file_identifier, multimedia_url_expiration):
        """
        Saves a message to the database

        Parameters:
        from_user: String
            username of the user who sent the message
        to_user: String
            username of the user who the message is sent to
        room: String
            name of the room
        content: String
            content of the message
        multimedia_url: String
            url of the multimedia if it exists
        multimedia_save_location: String
            location of the multimedia if it exists
        file_identifier: String
            unique identifier of the multimedia if it exists
        multimedia_url_expiration: String
            expiration time of the multimedia url if it exists

        Returns:
        Message
            Returns the saved message object    
        """
        from_user = User.objects.get(username=from_user)
        to_user = User.objects.get(username=to_user)
        room = Room.objects.get(slug=self.both_users_joined_room_name)

        saved_message = Message.objects.create(
            room=room,
            from_user=from_user, 
            to_user=to_user, 
            content=content,
            multimedia_url=multimedia_url,
            multimedia_save_location=multimedia_save_location,
            file_identifier=file_identifier,
            multimedia_url_expiration=multimedia_url_expiration
        )
        return saved_message
    
    @sync_to_async
    def get_or_create_room(self, room, username):
        """
        Get the room_name if it exists otherwise create it
        The room name is a combination of the two usernames
        e.g. if the two usernames are 'user1' and 'user2', 
        the room name will be 'user1-user2' or 'user2-user1', 
        which username comes first depends on who initiated 
        the first connection.
        Hence we will have to check for both combinations of
        usernames ('user1-user2' and 'user2-user1') as we don't 
        want duplicate rooms for the same two users.

        Parameters:
        room: String
            username of other user
        user: String
            username of authenticated user, the user
            who is requesting to join the chat room

        Returns:
        String
            Returns the slug of the room
        """
        room_name = "{}-{}".format(room, username)
        reverse_room_name = "{}-{}".format(username, room)

        # Create the Room if it does not exist
        if not Room.objects.filter(Q(slug=room_name) | Q(slug=reverse_room_name)).exists():
            Room.objects.create(slug=room_name, name=room_name)
        
        # Get the Room if it exists
        room = Room.objects.get(Q(slug=room_name) | Q(slug=reverse_room_name))
        # Saving the room in self
        self.room = room
        return room.slug
    

    async def chat_message(self, event):
        """
        Sends a WebSocket 'chat_message' event data back to the connected client.

        Parameters:
        - event (dict): WebSocket event data to be sent to the client.
        """
        await self.send(text_data=json.dumps(event))

    async def user_join(self, event):
        """
        Sends a WebSocket 'user_join' event data back to the connected client.

        Parameters:
        - event (dict): WebSocket event data to be sent to the client.
        """
        await self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        """
        Sends a WebSocket 'user_leave' event data back to the connected client.

        Parameters:
        - event (dict): WebSocket event data to be sent to the client.
        """
        await self.send(text_data=json.dumps(event))

class NotificationConsumer(AsyncWebsocketConsumer):
 
    async def connect(self):
        """
        Handles new WebSocket connection. Authenticates user,
        adds them to a notificaiton group, and sends the total
        number of unread messages the user has to the client.
        """

        self.notification_group_name = None

        self.user = self.scope.get("user")
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        await self.accept()

        # notification group
        self.notification_group_name = self.user.username + "__notifications"
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name,
        )
        
        # Send the total number of unread messages a user has
        unread_count = await sync_to_async(Message.objects.filter(to_user=self.user, read=False).count)()
        await self.send(text_data=json.dumps({
            "type": "unread_count",
            "unread_count": unread_count,
        }))
    

    async def disconnect(self, code):
        """
        Handles websocket disconnection. Removes the channel from 
        the group, and calls the superclass's disconnect method, 
        finalizing the disconnection process.

        Parameters:
        code: Integer
            Represents the WebSocket close code, indicating the reason for 
            closing the WebSocket connection
        """
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name,
        )
        
        # Calling the superclass's disconnect method
        # which finalizes the disconnection process.
        return super().disconnect(code)
    
    async def new_message_notification(self, event):
        """
        Sends a WebSocket 'new_message_notification' event data back to 
        the connected client.

        Parameters:
        - event (dict): WebSocket event data to be sent to the client.
        """
        await self.send(text_data=json.dumps(event))

    async def unread_count(self, event):
        """
        Sends a WebSocket 'unread_count' event data back to 
        the connected client.

        Parameters:
        - event (dict): WebSocket event data to be sent to the client.
        """
        await self.send(text_data=json.dumps(event))


class ConversationNotificationConsumer(AsyncWebsocketConsumer):
     
    async def connect(self):
        """
        Handles new WebSocket connection. Authenticates user,
        adds them to a per conversation notificaiton group, 
        and sends the number unread messages a user has in 
        a specific conversation/room to the client.
        """
        self.conversation_notification_group_name = None

        self.user = self.scope.get("user")
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        await self.accept()
        self.from_user = self.scope['url_route']['kwargs']['other_user']

        self.conversation_notification_group_name = self.from_user + self.user.username + "__conversation_notifications"
        await self.channel_layer.group_add(
            self.conversation_notification_group_name,
            self.channel_name,
        )
        
        # Get all the unread messages a user has from a particular user 
        # (the other user in the conversation/room) and send them
        from_user_model = await sync_to_async(get_user_model().objects.get)(username=self.from_user)
        unread_count = await sync_to_async(Message.objects.filter(to_user=self.user, from_user=from_user_model, read=False).count)()
        await self.send(text_data=json.dumps({
            "type": "single_conversation_unread_count",
            "unread_count": unread_count,   
        }))
    

    async def disconnect(self, code):
        """
        Handles websocket disconnection. Removes the channel from 
        the group, and calls the superclass's disconnect method, 
        finalizing the disconnection process.

        Parameters:
        code: Integer
            Represents the WebSocket close code, indicating the reason for 
            closing the WebSocket connection
        """
        await self.channel_layer.group_discard(
            self.conversation_notification_group_name,
            self.channel_name,
        )
        
        # Calling the superclass's disconnect method
        # which finalizes the disconnection process.
        return super().disconnect(code)
    
    async def single_conversation_new_message_notification(self, event):
        """
        Sends a WebSocket 'single_conversation_new_message_notification' 
        event data back to the connected client.

        Parameters:
        - event (dict): WebSocket event data to be sent to the client.
        """
        await self.send(text_data=json.dumps(event))

    async def single_conversation_unread_count(self, event):
        """
        Sends a WebSocket 'single_conversation_unread_count' 
        event data back to the connected client.

        Parameters:
        - event (dict): WebSocket event data to be sent to the client.
        """
        await self.send(text_data=json.dumps(event))

    async def single_conversation_last_message(self, event):
        """
        Sends a WebSocket 'last_message' event data back to 
        the connected client.

        Parameters:
        - event (dict): WebSocket event data to be sent to the client.
        """
        await self.send(text_data=json.dumps(event))


# For development purposes only
def generate_working_link_for_local_multimedia(multimedia_url):
    """
    Generates a working link for the multimedia_url

    Parameters:
    multimedia_url: String
        url of the multimedia

    Returns:
    String
        Returns the working link of the multimedia_url
    """
    
    multimedia_url = "http://{}:{}/chat-media/".format(env("HOST"), env("PORT")) + multimedia_url
    return multimedia_url