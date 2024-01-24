"""Room Tests"""
from channels.layers import get_channel_layer
from channels.testing import ChannelsLiveServerTestCase, WebsocketCommunicator
from django.contrib.auth import get_user_model
from asgiref.testing import ApplicationCommunicator
import json
from asgiref.sync import sync_to_async
from unittest.mock import Mock, patch
from cubeseed.room.models import Room
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from rest_framework.reverse import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from django.core.files.storage import default_storage
from datetime import datetime, timedelta
from .models import Message

from cubeseed.room.consumers import ChatConsumer, NotificationConsumer, ConversationNotificationConsumer

class ChatConsumerTest(ChannelsLiveServerTestCase):
    """
    ChatConsumer Tests
    """

    async def create_setup_communicator(self):
        """
        Sets up communicators and users.
        Six communicators are created:
        1. communicator - for testing the ChatConsumer (user)
        2. communicator_2 - for testing the ChatConsumer (user_2)
        3. communicator_notifications - for testing the NotificationConsumer (user)
        4. communicator_notifications_2 - for testing the NotificationConsumer (user_2)
        5. communicator_conversation_notification - for testing the per ConversationNotificationConsumer (user)
        6. communicator_conversation_notification_2 - for testing the per ConversationNotificationConsumer (user_2)
        """

        # Create test users
        user = await sync_to_async(get_user_model().objects.create_user)(username="testuser", password="testpassword", is_active=True)
        user_2 = await sync_to_async(get_user_model().objects.create_user)(username="testuser_2", password="testpassword_2", is_active=True)

        # Setup chat communicators
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/testuser_2/")
        communicator_2 = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/testuser/")

        # Setup the all conversations notification communicator
        communicator_notifications = WebsocketCommunicator(NotificationConsumer.as_asgi(), "/ws/notifications/")
        communicator_notifications_2 = WebsocketCommunicator(NotificationConsumer.as_asgi(), "/ws/notifications/")
        
        # Setup the per conversation notification communicator
        communicator_conversation_notification = WebsocketCommunicator(ConversationNotificationConsumer.as_asgi(), "/ws/notifications/testuser_2/")
        communicator_conversation_notification_2 = WebsocketCommunicator(ConversationNotificationConsumer.as_asgi(), "/ws/notifications/testuser/")

        # Adding user and url_route to the communicators scope
        # The steps below are required because this data is 
        # required by the consumer

        # Adding to the communicator scope
        communicator.scope['user'] = user 
        # communicator will be communicating with communicator_2
        communicator.scope['url_route'] = {'kwargs': {'room_name': 'testuser_2'}}

        # Adding to the communicator_2 scope
        communicator_2.scope['user'] = user_2
        # communicator_2 will be communicating with communicator
        communicator_2.scope['url_route'] = {'kwargs': {'room_name': 'testuser'}}

        # Adding to the notification communicator scope
        communicator_notifications.scope['user'] = user 
        communicator_notifications_2.scope['user'] = user_2

        # Adding to the the per conversation notification communicator scope
        communicator_conversation_notification.scope['user'] = user 
        communicator_conversation_notification.scope['url_route'] = {'kwargs': {'other_user': 'testuser_2'}}

        communicator_conversation_notification_2.scope['user'] = user_2
        communicator_conversation_notification_2.scope['url_route'] = {'kwargs': {'other_user': 'testuser'}}


        return {
            'user':user,
            'communicator':communicator, 
            'communicator_2':communicator_2,
            'communicator_notifications':communicator_notifications,
            'communicator_notifications_2':communicator_notifications_2,
            'communicator_conversation_notification':communicator_conversation_notification,
            'communicator_conversation_notification_2': communicator_conversation_notification_2
        }
    
    async def disconnect(self, communicator):
        """
        Disconnects the communicator from
        the websocket
        """
        await communicator.send_json_to({
            "type": "websocket.disconnect",
        })
        await communicator.disconnect()

    # Testing the connect method
    # Testing for succesful connection creation
    async def test_chat_consumer_connect(self):
        """
        Tests if a successful connection is created
        with the chat consumer
        """
        communicator_setup = await self.create_setup_communicator()
        communicator = communicator_setup['communicator']
        try:
            connected, _ = await communicator.connect()
            self.assertTrue(connected)
        finally:
            await self.disconnect(communicator)

    # Testing connect method
    # Testing the online_user_list event
    async def test_chat_consumer_connect_online_user_list_event(self):
        """
        Tests the online_user_list event of the connect method in the
        ChatConsumer
        """
        # Mock the query set returned by self.room.online.all()
        with patch('cubeseed.room.models.Room.online') as mock_online:
            user = await sync_to_async(get_user_model().objects.create_user)(username="testuser3", password="testpassword", is_active=True)
            user2 = await sync_to_async(get_user_model().objects.create_user)(username="testuser4", password="testpassword", is_active=True)
            mock_online.all.return_value = [user, user2]
            communicator_setup = await self.create_setup_communicator()
            communicator = communicator_setup['communicator']
            try:
                connected, _ = await communicator.connect()
                # recieving the online_user_list event
                response = await communicator.receive_json_from()

                self.assertEqual(response["type"], "online_user_list")
                self.assertEqual(response["users"], [user.username, user2.username])
            finally:
                await self.disconnect(communicator)

    # Testing connect method
    # Testing the user_join event
    async def test_chat_consumer_connect_user_join_event(self):
            """
            Tests the user_join event of the connect method in the
            ChatConsumer
            """
            communicator_setup = await self.create_setup_communicator()
            communicator = communicator_setup['communicator']
            user = communicator_setup['user']
            try:
                connected, _ = await communicator.connect()

                # This response gets the online_user_list event
                # The online_user_list event has to be retrieved
                # first in order to get access to the user_join
                # event.
                response = await communicator.receive_json_from()
                # This respone gets the user_join event
                response = await communicator.receive_json_from()
                self.assertEqual(response["type"], "user_join")
                self.assertEqual(response["user"], user.username)
            finally:
                await self.disconnect(communicator)

    # Testing recieve method          
    # Testing the read_messages event of the recieve method
    # Testing if all notifications consumer recives the event
    async def test_chat_consumer_recieve_read_messages_event_notfications(self):
        """
        Tests the read_messages event of the recieve method 
        in the ChatConsumer
        """
        communicator_setup = await self.create_setup_communicator()
        communicator = communicator_setup['communicator']
        communicator_notifications = communicator_setup['communicator_notifications']
        communicator_conversation_notification = communicator_setup['communicator_conversation_notification']
        try:
            try:
                connected, _ = await communicator.connect()
                connected, _ = await communicator_notifications.connect()
                connected, _ = await communicator_conversation_notification.connect()
            except Exception as e:
                print("printing connect exception: ", e)
            try:
                # Send a read_messages event to the ChatConsumer
                await communicator.send_json_to({
                    "type": "read_messages",
                })
            except Exception as e:
                print("printing send exception: ", e)

            # Check if the ChatConsumer has sent the appropriate response (unread_count)
            # to the notifications webscoket connection
            response = await communicator_notifications.receive_json_from()
            self.assertEqual(response["type"], "unread_count")
            self.assertEqual(response["unread_count"], 0)

            # Check if the ChatConsumer has sent the appropriate response 
            # (single_conversation_unread_count) to the per conversation 
            # notifications websocket connection
            response = await communicator_conversation_notification.receive_json_from()
            self.assertEqual(response["type"], "single_conversation_unread_count")
            self.assertEqual(response["unread_count"], 0)
        finally:
            await self.disconnect(communicator)
            await self.disconnect(communicator_notifications)
            await self.disconnect(communicator_conversation_notification)

    # Testing the chat message event of the recieve method
    async def test_chat_consumer_recieve_chat_message_event(self):
        """
        Tests the chat_message event in the recieve method of 
        the ChatConsumer
        """
        communicator_setup = await self.create_setup_communicator()
        communicator = communicator_setup['communicator']
        communicator_2 = communicator_setup['communicator_2']
        try:
            try:
                connected, _ = await communicator.connect()
                connected, _ = await communicator_2.connect()

                # The following two events have to be retrieved
                # first inorder to get access to the chat_message
                # event
                 
                # This response gets the online_user_list event
                response = await communicator_2.receive_json_from()
                # This response get the user_join event
                response = await communicator_2.receive_json_from()
            except Exception as e:
                print("printing connect exception: ", e)
            # communicator sending a chat message to communicator_2
            try:
                await communicator.send_json_to({
                    "type": "chat_message",
                    "message": "Hello, world!",
                    "multimedia_url": "multimedia url link",
                    "file_identifier": "",
                    "multimedia_url_expiration": "",
                })
            except Exception as e:
                print("printing send exception: ", e)

            # Checking if communicator_2 has successfully recieved the
            # chat_message
            response = await communicator_2.receive_json_from()
            self.assertEqual(response["message"], "Hello, world!")
        finally:
            await self.disconnect(communicator)
            await self.disconnect(communicator_2)


    # Testing if a new message notification will be sent
    # when a chat_message event is recieved 
    async def test_chat_consumer_chat_message_event_new_message_notification(self):
        """
        Testing if a new message notification will be sent
        when a chat_message event is recieved 
        """
        communicator_setup = await self.create_setup_communicator()
        communicator_notifications_2 = communicator_setup['communicator_notifications_2']
        communicator = communicator_setup['communicator']

        try:
            try:
                connected, _ = await communicator.connect()
                connected, _ = await communicator_notifications_2.connect()
            except Exception as e:
                print("printing connect exception: ", e)

            # communicator sending a chat message to communicator_2
            await communicator.send_json_to({
                "type": "chat_message",
                "message": "Hello, world!",
                "multimedia_url": "multimedia url link",
                "file_identifier": "",
                "multimedia_url_expiration": "",
            })

            # Checking if user_2 has recieved the new_message_notification         

            # This response gets the unread_count event sent by the
            # notification consumer, it has to be retrieved first 
            # in order to get access to the new_message_notification
            # event
            response = await communicator_notifications_2.receive_json_from()
            # This response gets the new_message_notification event
            response = await communicator_notifications_2.receive_json_from()
            self.assertEqual(response["type"], "new_message_notification")
        finally:
            await self.disconnect(communicator)
            await self.disconnect(communicator_notifications_2)


    # Testing if a per conversation new message notification 
    # will be sent when a chat_message event is recieved 
    async def test_chat_consumer_chat_message_event_new_message_conversation_notification(self):
        """
        Testing if a per conversation new message notification 
        will be sent when a chat_message event is recieved 
        """
        communicator_setup = await self.create_setup_communicator()
        communicator = communicator_setup['communicator']
        communicator_conversation_notification_2 = communicator_setup['communicator_conversation_notification_2']
        try:
            try:
                connected, _ = await communicator.connect()
                connected, _ = await communicator_conversation_notification_2.connect()
            except Exception as e:
                print("printing connect exception: ", e)
            
            await communicator.send_json_to({
                "type": "chat_message",
                "message": "Hello, world!",
                "multimedia_url": "multimedia url link",
                "file_identifier": "",
                "multimedia_url_expiration": "",
                "room": "testuser",
            })
            # This response gets the single_conversation_unread_count event
            # It has to be retrieved first in order to get access to the 
            # single_conversation_new_message_notification event
            response = await communicator_conversation_notification_2.receive_json_from()
            # This response gets the single_conversation_new_message_notification event
            response = await communicator_conversation_notification_2.receive_json_from()
            self.assertEqual(response["type"], "single_conversation_new_message_notification")
        finally:
            await self.disconnect(communicator)
            await self.disconnect(communicator_conversation_notification_2)


    # Testing if the details of the last message in a conversation 
    # are sent when a chat_message event is recieved  
    async def test_chat_consumer_chat_message_event_last_message_conversation_notification(self):
        """
        Testing if the details of the last message in a conversation 
        are sent when a chat_message event is recieved  
        """
        communicator_setup = await self.create_setup_communicator()
        communicator = communicator_setup['communicator']
        communicator_conversation_notification_2 = communicator_setup['communicator_conversation_notification_2']
        try:
            try:
                connected, _ = await communicator.connect()
                connected, _ = await communicator_conversation_notification_2.connect()
            except Exception as e:
                print("printing connect exception: ", e)
            
            await communicator.send_json_to({
                "type": "chat_message",
                "message": "Hello, world!",
                "multimedia_url": "multimedia url link",
                "file_identifier": "",
                "multimedia_url_expiration": "",
                "room": "testuser",
            })
            # These responses gets the single_conversation_unread_count event
            # and the single_conversation_new_message_notification event
            # They have to be retrieved first in order to get access to the 
            # single_conversation_last_message event
            response = await communicator_conversation_notification_2.receive_json_from()
            response = await communicator_conversation_notification_2.receive_json_from()
            # This response gets the single_conversation_last_message event
            response = await communicator_conversation_notification_2.receive_json_from()
            self.assertEqual(response["type"], "single_conversation_last_message")
            self.assertEqual(response["last_message"], "Hello, world!")
        finally:
            await self.disconnect(communicator)
            await self.disconnect(communicator_conversation_notification_2)

# Testing the notification consumer
class NotificationConsumerTest(ChannelsLiveServerTestCase):
    """
    NotificationConsumer Tests
    """

    async def create_setup_communicator(self):
        """
        Setup a notifications communicator and a user
        """
        # Create a test user
        user = await sync_to_async(get_user_model().objects.create_user)(username="testuser", password="testpassword", is_active=True)
        # Setup the all notifications communicator
        communicator_notifications = WebsocketCommunicator(NotificationConsumer.as_asgi(), "/ws/notifications/")

        # Adding user communicator's scope
        # The steps below is required because this data is 
        # required by the consumer
        communicator_notifications.scope['user'] = user 

        return {
                'user':user,
                'communicator_notifications':communicator_notifications
                }
    
    async def disconnect(self, communicator):
        """
        Disconnects the communicator from 
        the websocket
        """
        await communicator.send_json_to({
            "type": "websocket.disconnect",
        })
        await communicator.disconnect()

    # Testing the connect method
    # Testing for succesful connection creation
    async def test_notification_consumer_connect(self):
        """
        Testing the connect method of the NotificationConsumer
        Tests for succesful connection creation
        """
        communicator_setup = await self.create_setup_communicator()
        communicator_notifications = communicator_setup['communicator_notifications']
        connected, _ = await communicator_notifications.connect()
        self.assertTrue(connected)
        await self.disconnect(communicator_notifications)

    # Testing connect method
    # Testing the unread_count event
    async def test_notification_consumer_connect_unread_count_event(self):
        """
        Tests if the unread_count event is sent when
        a user connects to the NotificationConsumer
        """
        communicator_setup = await self.create_setup_communicator()
        communicator_notifications = communicator_setup['communicator_notifications']
        connected, _ = await communicator_notifications.connect()
        response = await communicator_notifications.receive_json_from()
        self.assertEqual(response["type"], "unread_count")
            
# Testing the conversation notification consumer
class ConversationNotiificationConsumerTest(ChannelsLiveServerTestCase):
    """
    ConversationNotificationConsumer Tests
    """
    async def create_setup_communicator(self):
        """
        Setup a conversation notifications communicator and a user
        """
        # Create a test user
        user = await sync_to_async(get_user_model().objects.create_user)(username="testuser", password="testpassword", is_active=True)
        user_notification = await sync_to_async(get_user_model().objects.create_user)(username="testuser_notification", password="testpassword", is_active=True)

        # Setup the per conversation notification communicator
        communicator_conversation_notification = WebsocketCommunicator(ConversationNotificationConsumer.as_asgi(), "/ws/notifications/testuser_notification/")

        # Adding user and url_route to the communicator's scope
        # The steps below are required because this data is 
        # required by the consumer
        communicator_conversation_notification.scope['user'] = user 
        communicator_conversation_notification.scope['url_route'] = {'kwargs': {'other_user': 'testuser_notification'}}
        return { 
                'user':user,  
                'communicator_conversation_notification':communicator_conversation_notification
                }
    
    async def disconnect(self, communicator):
        """
        Disconnects the communicator from
        the websocket
        """
        await communicator.send_json_to({
            "type": "websocket.disconnect",
        })
        await communicator.disconnect()

    # Testing the connect method
    # Testing for succesful connection creation
    async def test_conversation_notification_consumer_connect(self):
        """
        Testing the connect method of the ConversationNotificationConsumer
        Tests for succesful connection creation
        """
        communicator_setup = await self.create_setup_communicator()
        communicator_conversation_notification = communicator_setup['communicator_conversation_notification']
        connected, _ = await communicator_conversation_notification.connect()
        self.assertTrue(connected)
        await self.disconnect(communicator_conversation_notification)

    # Testing connect method
    # Testing the single_conversation_unread_count event
    async def test_conversation_notification_consumer_connect_unread_count_event(self):
        """
        Tests if the single_conversation_unread_count 
        event is sent when a user connects to the 
        ConversationNotificationConsumer
        """
        communicator_setup = await self.create_setup_communicator()
        communicator_conversation_notification = communicator_setup['communicator_conversation_notification']
        connected, _ = await communicator_conversation_notification.connect()
        response = await communicator_conversation_notification.receive_json_from()
        self.assertEqual(response["type"], "single_conversation_unread_count")


# Testing APIs related to chat
User = get_user_model()
class APIsTest(APITestCase):
    """
    Tests API's related to chat
    """
    def setUp(self) -> None:
        """
        setup that is run before every test
        """
        # Create a user
        self.user = User.objects.create_user(username="testuserapi", password="testpasswordapi")
        self.user.is_active = True
        self.user.groups.add(Group.objects.get(name="farmer"))
        self.user.save()

    def authenticate(self):
        """
        Authenticates a user, and obtains an access
        token
        """
        token_response = self.client.post(
            reverse("token_obtain_pair"), {"username": "testuserapi", "password": "testpasswordapi"}
        )
        access_token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_dev_upload_endpoint(self):
        """
        Test if a multimedia file is uploaded successfully
        (using the dev environment)
        """
        # Mock the default_storage.save method
        # Mock the setting.DEBUG variable
        with patch.object(default_storage, 'save', return_value='saved_test_file.txt'):
            with patch('django.conf.settings.DEBUG') as mock_debug:
                mock_debug.return_value = True
                
                # authenticate the user
                self.authenticate()

                # Create a sample file to upload
                file_content = b'This is the content of the file.'
                uploaded_file = SimpleUploadedFile("test_file.txt", file_content, content_type="text/plain")

                # Prepare the form data
                data = {'myFile': uploaded_file}

                # Make a POST request to the uploads endpoint
                response = self.client.post(reverse("uploads"), data, format="multipart")
                json_response = response.json()
                
                self.assertEqual(
                    response.status_code,
                    status.HTTP_200_OK,
                    msg=f"Failed to upload file",
                )
                self.assertEqual(
                    json_response["file_location"],
                    "saved_test_file.txt",
                    msg=f"file_location is not correct",
                )
                self.assertEqual(
                    json_response["file_identifier"],
                    "saved_test_file.txt",
                    msg=f"file_identifier is not correct",
                )
                self.assertEqual(
                    json_response["expiration_time"],
                    None,
                    msg=f"expiration_time is not correct",
                )
                

    def test_prod_upload_endpoint(self):
        """
        Test if a multimedia file is uploaded successfully
        (using the prod environment) 
        """
        # Mock the default_storage.save method
        # Mock the datetime.now() method
        # Mock the generate_presigned_url method
        formated_datetime = datetime.strptime("2024-01-02 15:22:12.780359", '%Y-%m-%d %H:%M:%S.%f')
        with patch.object(default_storage, 'save', return_value='saved_test_file.txt'):
            with patch('cubeseed.room.views.datetime') as mock_datetime:
                with patch('cubeseed.room.views.generate_presigned_url') as mock_generate_presigned_url:
                    # settings.DEBUG is not mocked because its returning False by default
                    # (which is production mode)
                    mock_generate_presigned_url.return_value = "http://aws-generated-presigned-url.com"
                    mock_datetime.now.return_value=formated_datetime
                    # authenticate the user
                    self.authenticate()

                    # Create a sample file to upload
                    file_content = b'This is the content of the file.'
                    uploaded_file = SimpleUploadedFile("test_file.txt", file_content, content_type="text/plain")

                    # Prepare the form data
                    data = {'myFile': uploaded_file}

                    # Make a POST request to the uploads endpoint
                    response = self.client.post(reverse("uploads"), data, format="multipart")
                    json_response = response.json()
                    test_expiration_time = formated_datetime + timedelta(days=1)

                    self.assertEqual(
                        response.status_code,
                        status.HTTP_200_OK,
                        msg=f"Failed to upload file",
                    )
                    self.assertEqual(
                        json_response["file_location"],
                        "http://aws-generated-presigned-url.com",
                        msg=f"file_location is not correct",
                    )
                    self.assertEqual(
                        json_response["file_identifier"],
                        "saved_test_file.txt",
                        msg=f"file_identifier is not correct",
                    )
                    self.assertEqual(
                        json_response["expiration_time"],
                        test_expiration_time.isoformat(),
                        msg=f"expiration_time is not correct",
                    )
  

    # Testing the url validity checker
    # /api/rooms/check-url/?message_id=${message_id}
    def test_check_dev_url_validity_endpoint(self):
        """
        Checks if the multimedia url has not expired
        (using dev environment)
        """

        mock_room = Room (
            name = "test_room",
            slug = "test_room",
        )

       # Create testuser_2
        self.user_2 = User.objects.create_user(username="testuser_2api", password="testuser_2passwordapi")
        self.user_2.is_active = True
        self.user_2.groups.add(Group.objects.get(name="farmer"))
        self.user_2.save()
        
        mock_message = Message(
            id = 1,
            room = mock_room,
            from_user = self.user,
            to_user = self.user_2,
            content = "test_message content",
            multimedia_url = "http://multimedia_url.com",
            multimedia_save_location = "local",
            file_identifier = "multimedia_url.txt",
            multimedia_url_expiration = "2024-01-02 15:22:12.780359",
        )
        # Mock the Message.objects.get method
        with patch('cubeseed.room.views.Message') as mock_get_message:
            mock_get_message.objects.get.return_value = mock_message

            # authenticate the user
            self.authenticate()

            # Make a GET request to the check-url endpoint
            url  = reverse("check-url")
            response = self.client.get(url, format="json")
            json_response = response.json()
            # False is being checked for because during development
            # the multimedia url does not expire, as it is saved locally
            # (AWS presigned urls are not used during development)
            self.assertFalse(json_response["refresh_url"])

    def test_check_prod_url_validity_endpoint_unexpired_link(self):
        """
        Checks if the multimedia url has not expired
        (using prod environment)
        """
        mock_room = Room (
            name = "test_room",
            slug = "test_room",
        )

       # Create testuser_2
        self.user_2 = User.objects.create_user(username="testuser_2api", password="testuser_2passwordapi")
        self.user_2.is_active = True
        self.user_2.groups.add(Group.objects.get(name="farmer"))
        self.user_2.save()
        
        mock_message = Message(
            id = 1,
            room = mock_room,
            from_user = self.user,
            to_user = self.user_2,
            content = "test_message content",
            multimedia_url = "http://multimedia_url.com",
            multimedia_save_location = "s3",
            file_identifier = "multimedia_url.txt",
            multimedia_url_expiration = "2024-01-02 15:22:12.780359",
        )

        # Mock the Message.objects.get method
        # Mock the datetime.now() and datetime.fromisoformat() methods
        with patch('cubeseed.room.views.Message') as mock_get_message:
            formated_now_datetime = datetime.strptime("2024-01-05 15:22:12.780359", '%Y-%m-%d %H:%M:%S.%f')
            formated_saved_datetime = datetime.strptime("2024-01-06 15:22:12.780359", '%Y-%m-%d %H:%M:%S.%f')
            with patch('cubeseed.room.views.datetime', spec=datetime) as mock_datetime:
                mock_datetime.now.return_value=formated_now_datetime
                # The fromisoformat had to be mocked because of the following error
                # TypeError: '<' not supported between instances of 'MagicMock' and 'datetime.datetime'
                mock_datetime.fromisoformat.return_value=formated_saved_datetime
                mock_get_message.objects.get.return_value = mock_message

                # authenticate the user
                self.authenticate()

                # Make a GET request to the check-url endpoint
                url  = reverse("check-url")
                response = self.client.get(url, format="json")
                json_response = response.json()
                # The response is expected to be false because the
                # multimedia url has not expired
                self.assertFalse(json_response["refresh_url"])

    def test_check_prod_url_validity_endpoint_expired_link(self):
        """
        Checks if the multimedia url has expired
        (using prod environment)
        """
        mock_room = Room (
            name = "test_room",
            slug = "test_room",
        )

       # Create testuser_2
        self.user_2 = User.objects.create_user(username="testuser_2api", password="testuser_2passwordapi")
        self.user_2.is_active = True
        self.user_2.groups.add(Group.objects.get(name="farmer"))
        self.user_2.save()
        
        mock_message = Message(
            id = 1,
            room = mock_room,
            from_user = self.user,
            to_user = self.user_2,
            content = "test_message content",
            multimedia_url = "http://multimedia_url.com",
            multimedia_save_location = "s3",
            file_identifier = "multimedia_url.txt",
            multimedia_url_expiration = "2024-01-02 15:22:12.780359",
        )
        # Mock the Message.objects.get method
        # Mock the datetime.now() and datetime.fromisoformat() methods
        with patch('cubeseed.room.views.Message') as mock_get_message:
            formated_now_datetime = datetime.strptime("2024-01-06 15:22:12.780359", '%Y-%m-%d %H:%M:%S.%f')
            formated_saved_datetime = datetime.strptime("2024-01-05 15:22:12.780359", '%Y-%m-%d %H:%M:%S.%f')
            with patch('cubeseed.room.views.datetime', spec=datetime) as mock_datetime:
                mock_datetime.now.return_value=formated_now_datetime
                # The fromisoformat had to be mocked because of the following error
                # TypeError: '<' not supported between instances of 'MagicMock' and 'datetime.datetime'
                mock_datetime.fromisoformat.return_value=formated_saved_datetime
                mock_get_message.objects.get.return_value = mock_message

                # authenticate the user
                self.authenticate()

                # Make a GET request to the check-url endpoint
                url  = reverse("check-url")
                response = self.client.get(url, format="json")
                json_response = response.json()
                # The response is expected to be true because the
                # multimedia url has expired
                self.assertTrue(json_response["refresh_url"])


    # Testing the url refresh endpoint
    # /api/rooms/refresh-url/?message_id=${message_id}
    def test_url_refresh_endpoint(self):
        """
        Refreshes the expired multimedia url
        """
        mock_room = Room (
            name = "test_room",
            slug = "test_room",
        )

       # Create testuser_2
        self.user_2 = User.objects.create_user(username="testuser_2api", password="testuser_2passwordapi")
        self.user_2.is_active = True
        self.user_2.groups.add(Group.objects.get(name="farmer"))
        self.user_2.save()
        
        # Mock the Message.objects.get method
        mock_message = Message(
            id = 1,
            room = mock_room,
            from_user = self.user,
            to_user = self.user_2,
            content = "test_message content",
            multimedia_url = "http://multimedia_url.com",
            multimedia_save_location = "s3",
            file_identifier = "multimedia_url.txt",
            multimedia_url_expiration = "2024-01-02 15:22:12.780359",
        )
        # Mock the Message.objects.get method
        # Mock the datetime.now() method
        # Mock the cubeseed.room.views.generate_presigned_url method
        with patch('cubeseed.room.views.Message') as mock_get_message:
            formated_now_datetime = datetime.strptime("2024-01-06 15:22:12.780359", '%Y-%m-%d %H:%M:%S.%f')
            with patch('cubeseed.room.views.datetime', spec=datetime) as mock_datetime:
                with patch('cubeseed.room.views.generate_presigned_url') as mock_generate_presigned_url:
                    with patch('cubeseed.room.models.Message.save') as mock_message_save:
                        mock_datetime.now.return_value=formated_now_datetime
                        mock_get_message.objects.get.return_value = mock_message
                        mock_generate_presigned_url.return_value = "http://aws-refreshed-presigned-url.com"
                        mock_message_save.return_value = None

                        # authenticate the user
                        self.authenticate()

                        # Make a GET request to the refresh-url endpoint
                        url  = reverse("refresh-url")
                        response = self.client.get(url, format="json")
                        json_response = response.json()
                        self.assertEqual(json_response["file_location"], "http://aws-refreshed-presigned-url.com")

    # Testing the get all conversation endpoint
    # /api/conversations
    def test_get_all_conversations_endpoint(self):
        """
        Tests if all conversations of a user are
        fetched successfully
        """
        # Create testuser_2
        self.user_2 = User.objects.create_user(username="testuser_2api", password="testuser_2passwordapi")
        self.user_2.is_active = True
        self.user_2.groups.add(Group.objects.get(name="farmer"))
        self.user_2.save()

        # Create testuser_3
        self.user_3 = User.objects.create_user(username="testuser_3api", password="testuser_3passwordapi")
        self.user_3.is_active = True
        self.user_3.groups.add(Group.objects.get(name="farmer"))
        self.user_3.save()

        # Create a room were testuserapi and testuser_2api are members
        mock_room = Room (
            name = "testuserapi-testuser_2api",
            slug = "testuserapi-testuser_2api",
        )
        mock_room.save()

        # Create a room were testuserapi and testuser_3api are members
        mock_room_2 = Room (
            name = "testuserapi-testuser_3api",
            slug = "testuserapi-testuser_3api",
        )
        mock_room_2.save()

        # Create a room  were testuserapi and testuserapi are members
        # This room is for self conversation
        mock_room3 = Room (
            name = "testuserapi-testuserapi",
            slug = "testuserapi-testuserapi",
        )
        mock_room3.save()

        # Create a room were self.testuser_2api and testuser_3api are members
        mock_room4 = Room (
            name = "testuser_2api-testuser_3api",
            slug = "testuser_2api-testuser_3api",
        )
        mock_room4.save()

        # authenticate the user
        self.authenticate()

        # Make a GET request to the get list of conversations endpoint
        url  = reverse("conversations")
        response = self.client.get(url, format="json")
        json_response = response.json()

        # Two responses are expected because testuserapi has 2 conversations,
        # the room where testuserapi is having a conversation with itself
        # is not supposed to be included
        self.assertEqual(
            json_response["count"],
            2
        )
        self.assertEqual(
            json_response["results"][0]["name"], 
            "testuserapi-testuser_2api"
        )
        self.assertEqual(
            json_response["results"][1]["name"], 
            "testuserapi-testuser_3api"
        )

    


    # Testing the get all messages within a room endpoint, where 
    # the room exists, the users have had a conversation previously
    # /api/rooms/${room}/messages
    # Case1: The room was created by the name testuser_2api-testuserapi
    # (logged in user is testuserapi)
    def test_get_all_messages_within_a_room_endpoint_case1(self):
        """
        Testing case1 of the get all messages within a room endpoint
        
        Tests if all messages within a room can be fetched
        successfully in the case where the users have had prior
        conversation and the room name is testuser_2api-testuserapi,
        this means testuser_2api initiated the first connection
        with testuserapi.
        The logged in user is testuserapi)
        """

        # Create testuser_2
        self.user_2 = User.objects.create_user(username="testuser_2api", password="testuser_2passwordapi")
        self.user_2.is_active = True
        self.user_2.groups.add(Group.objects.get(name="farmer"))
        self.user_2.save()

        # authenticate testuserapi user
        self.authenticate()
        room = Room (
            name = "testuser_2api-testuserapi",
            slug = "testuser_2api-testuserapi",
        )
        room.save()
        
        # Create a Message object and save it
        message = Message(
            id = 1,
            room = room,
            from_user = self.user,
            to_user = self.user_2,
            content = "test_message content",
            multimedia_url = "http://multimedia_url.com",
            multimedia_save_location = "s3",
            file_identifier = "multimedia_url.txt",
            multimedia_url_expiration = "2024-01-02 15:22:12.780359",
        )
        message.save()

        # Make a GET request to the /api/rooms/${room}/messages endpoint
        url  = reverse("room", kwargs={"slug": self.user_2.username})
        response = self.client.get(url, format="json")
        json_response = response.json()
        self.assertEqual(len(json_response["messages"]), 1)
        self.assertEqual(json_response["messages"][0]["from_user"]["username"], "testuserapi")
        self.assertEqual(json_response["messages"][0]["to_user"]["username"], "testuser_2api")
        self.assertEqual(json_response["messages"][0]["content"], "test_message content")

    # Testing the get all messages within a room endpoint, where 
    # the room exists, the users have had a conversation previously
    # /api/rooms/${room}/messages
    # Case 2: The room was created by the name testuserapi-testuser_2api
    # (logged in user is testuserapi)
    def test_get_all_messages_within_a_room_endpoint_case2(self):
        """
        Testing case2 of the get all messages within a room endpoint

        Tests if all messages within a room can be fetched
        successfully in the case where the users have had prior
        conversation and the room name is testuserapi-testuser_2api,
        this means testuserapi initiated the first connection
        with testuser_2api.
        The logged in user is testuserapi)
        """

        # Create testuser_2
        self.user_2 = User.objects.create_user(username="testuser_2api", password="testuser_2passwordapi")
        self.user_2.is_active = True
        self.user_2.groups.add(Group.objects.get(name="farmer"))
        self.user_2.save()

        # authenticate the user
        self.authenticate()

        room = Room (
            name = "testuserapi-testuser_2api",
            slug = "testuserapi-testuser_2api",
        )
        room.save()
        
        # Create a Message object and save it
        message = Message(
            id = 1,
            room = room,
            from_user = self.user,
            to_user = self.user_2,
            content = "test_message content",
            multimedia_url = "http://multimedia_url.com",
            multimedia_save_location = "s3",
            file_identifier = "multimedia_url.txt",
            multimedia_url_expiration = "2024-01-02 15:22:12.780359",
        )
        message.save()

        # Make a GET request to the /api/rooms/${room}/messages endpoint
        url  = reverse("room", kwargs={"slug": self.user_2.username})
        response = self.client.get(url, format="json")
        json_response = response.json()
        self.assertEqual(len(json_response["messages"]), 1)
        self.assertEqual(json_response["messages"][0]["from_user"]["username"], "testuserapi")
        self.assertEqual(json_response["messages"][0]["to_user"]["username"], "testuser_2api")
        self.assertEqual(json_response["messages"][0]["content"], "test_message content")


    # Testing the get all messages within a room endpoint
    # /api/rooms/${room}/messages
    # Case 3: Users have no prior conversation
    def test_get_all_messages_within_a_room_endpoint_case3(self):
        """
        Testing case3 of the get all messages within a room endpoint

        Tests if no messages are fetched in the case where the 
        users do not have prior conversation
        """

        # Create testuser_2
        self.user_2 = User.objects.create_user(username="testuser_2api", password="testuser_2passwordapi")
        self.user_2.is_active = True
        self.user_2.groups.add(Group.objects.get(name="farmer"))
        self.user_2.save()

        # authenticate the user
        self.authenticate()

        # Make a GET request to the /api/rooms/${room}/messages endpoint
        url  = reverse("room", kwargs={"slug": self.user_2.username})
        response = self.client.get(url, format="json")
        json_response = response.json()
        self.assertEqual(json_response["messages"], [])
