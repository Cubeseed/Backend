"""Room Views"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
# from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from .serializer import MessageSerializer
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from .serializer import ConversationSerializer
from rest_framework.parsers import MultiPartParser
from django.conf import settings
import os
from django.core.files.storage import default_storage
from datetime import datetime, timedelta
from botocore.exceptions import NoCredentialsError
import environ
import boto3
from .models import Message
from django.conf import settings
from django.contrib.auth import get_user_model

env = environ.Env()
env.read_env()

User = get_user_model()

# # Create your views here.
# @permission_classes([IsAuthenticated])
# def rooms(request):
#     rooms = User.objects.all()
#     return render(request, "room/rooms.html", {"rooms": rooms})

# @permission_classes([IsAuthenticated])
# def room(request, slug):
#     # Get username
#     username = request.user.username

#     room_name = "{}-{}".format(slug, username)
#     reverse_room_name = "{}-{}".format(username, slug)

#     # Create the Room if it does not exist
#     if not Room.objects.filter(Q(slug=room_name) | Q(slug=reverse_room_name)).exists():
#         Room.objects.create(slug=room_name, name=room_name)

#     room = Room.objects.get(Q(slug=room_name) | Q(slug=reverse_room_name))
#     messages = Message.objects.filter(room=room)[0:25]
#     return render(request, "room/room.html", {"room": room, "messages": messages})


class MessagesApi(APIView):
    """
    View for getting all messages in a room
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer
    def get(self, request, slug):
        """
        Retrieves all messages from a room specified by the slug. 
        If the room does not exist, it creates one.
        
        Parameters:
            request: HttpRequest
                The request object.
            slug: String
                The slug representing the room, obtained from the URL.

        Returns:
        JsonResponse
            A JSON response containing all messages in the room.
        """
        # Get user
        user = self.request.user

        room_name = "{}-{}".format(slug, user)
        reverse_room_name = "{}-{}".format(user, slug)

        # Create the Room if it does not exist
        if not Room.objects.filter(Q(slug=room_name) | Q(slug=reverse_room_name)).exists():
            Room.objects.create(slug=room_name, name=room_name)

        room = Room.objects.get(Q(slug=room_name) | Q(slug=reverse_room_name))

        serializer = MessageSerializer(Message.objects.filter(room=room), 
                                       many=True,
                                       context={'request': request})
        return JsonResponse({"messages": serializer.data})


# class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
class ConversationViewSet(ListModelMixin, GenericViewSet):
    """
    Viewset for getting all conversations a user
    has
    """
    serializer_class = ConversationSerializer
    queryset = Room.objects.none()
    # lookup_field = "name"

    def get_queryset(self):
        """
        Getting all conversations a user has, excluding
        conversations with self

        Returns:
        QuerySet
            Returns all the conversations a user had with other
            users
        """
        # Getting all conversations
        queryset = Room.objects.filter(
            name__contains=self.request.user.username
        ).exclude(
            # Exclude conversation with self
            name__contains="{}-{}".format(self.request.user.username, self.request.user.username)    
        )
        return queryset
    
    def get_serializer_context(self):
        """
        Passes a context dictionary that contains the request and user
        associated with the request to the serializer class.

        Returns:
        Disctionary
            Returns a dictionary containing the request and user
            associated with the request
        """
        # The request is added to the context in ordert to avoid the
        # following error:
        # AssertionError: `HyperlinkedIdentityField` requires the request
        # in the serializer context. Add `context={'request': request}` 
        # when instantiating the serializer.
        return {"request": self.request, "user": self.request.user}
    
    # def retrieve(self, request, name=None):
    #     user = self.request.user
    #     room_name = "{}-{}".format(name, user)
    #     reverse_room_name = "{}-{}".format(user, name)

    #     room = Room.objects.get(Q(slug=room_name) | Q(slug=reverse_room_name))

    #     serializer = ConversationSerializer(room, context={"request": request, "user": user})
    #     return JsonResponse({"room": serializer.data})

class UploadEndpoint(APIView):
    """
    View for uploading multimedia
    """
    parser_classes = (MultiPartParser,)

    def post(self, request):
        """
        post method for saving multimedia files. Files can be
        stored locally (dev mode) or in an s3 bucket (AWS) (Prod mode)

        Parameters:
        request: Request
            The request object

        Returns:
        JsonResponse
            A JSON response containing the file location, expiration time
            and file identifier.
            In production mode file_location is a presigned url, while in
            development mode the file_location is the same as the file 
            identifier.
        """
        file = request.FILES['myFile']
        # Save the file to the default storage location
        # For production mode, the default storage location is an s3 bucket
        # For development mode, the default storage location is the local file system
        file_path = default_storage.save(file.name, file)
        # A unique file identifier
        file_identifier = file_path
        # Custom Expiration time (1 day)
        expiration_time = datetime.now() + timedelta(days=1)
        if settings.DEBUG == False:
            # The server is in production mode
            # Generate an AWS presigned URL for the file
            presigned_url = generate_presigned_url(file_path, expiration_time)

            return JsonResponse({'file_location': presigned_url,
                                'expiration_time': expiration_time.isoformat(),
                                'file_identifier': file_identifier,
                                })
        else:
            # The server is in development mode
            # File is is saved locally
            return JsonResponse({'file_location': file_path,
                    'expiration_time': None,
                    'file_identifier': file_path,
                    })
    
class RefreshURLView(APIView):
    """
    View for refreshing a URL
    """
    def get(self, request):
        """
        get method for refreshing an expired URL (AWS presigned URL)

        Parameters:
        request: Request
            The request object

        Returns:
        JsonResponse
            A JSON response containing the file_location (refreshed AWS 
            presigned url).
        """

        # Getting the message_id from the request
        message_id = request.GET.get('message_id')

        # Get the message object from the database
        message_object = Message.objects.get(id=message_id)

        # Set the expiration time to 1 day from now
        expiration_time = datetime.now() + timedelta(days=1)

        # Generate a new presigned URL with the updated expiration time
        try:
            refreshed_url = generate_presigned_url(message_object.file_identifier, expiration_time)

            # Update the message object with the new expiration time and refreshed url
            message_object.multimedia_url = refreshed_url
            message_object.multimedia_url_expiration = expiration_time.isoformat()
            message_object.save()
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'file_location': message_object.multimedia_url})
    
class CheckURLView(APIView):
    """
    View for checking if a URL has expired
    """
    def get(self, request):
        """
        get method for checking if a URL has expired

        Parameters:
        request: Request
            The request object
        
        Returns:
        JsonResponse
            A JSON response containing a boolean value indicating if the
            URL has expired or not. If the presigned URL has expired, the 
            response will be True, otherwise it will be False.

            In the case where multimedia is saved locally, the response
            will always be False (as it does not have a presigned url, it 
            will not need refreshing).
        """
        # Getting the message_id from the request object
        message_id = request.GET.get('message_id')
        
        # Get the message and check if the media url has expired
        message = Message.objects.get(id=message_id)

        # Check if the multimedia link is a local link or an s3 link
        if message.multimedia_save_location == 'local':
            # Does not need refreshing
            return JsonResponse({'refresh_url': False})
    
        elif message.multimedia_save_location == 's3':
            # It is an AWS presigned url keep on checking the other requirements
            if datetime.fromisoformat(message.multimedia_url_expiration) < datetime.now():
                # The presigned url has expired, return True
                return JsonResponse({'refresh_url': True})
            else:
                # The presigned url has not expired, return False
                return JsonResponse({'refresh_url': False})
        

def generate_presigned_url(file_identifier, expiration_time):
    """
    Given a file path and an expiration time, generates an
    AWS presigned URL.

    Parameters:
        file_identifier: String
            The identifier to the file in the s3 bucket
        expiration_time: Datetime
            The desired expiration time for the presigned URL

    Returns:
    String
        Returns the presigned URL
    """
    s3_client = boto3.client('s3',
        aws_access_key_id=env("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=env("AWS_SECRET_ACCESS_KEY"),
        config=boto3.session.Config(
            signature_version='s3v4',
            region_name=env("AWS_S3_REGION_NAME"),
        ))

    try:
        # Generate a presigned URL with the specified expiration time
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': env("AWS_STORAGE_BUCKET_NAME"), 'Key': file_identifier},
            ExpiresIn=int((expiration_time - datetime.utcnow()).total_seconds())
        )

        return presigned_url

    except NoCredentialsError as e:
        return JsonResponse({'error': 'AWS credentials not available.'}, status=500)