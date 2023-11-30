from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth.models import User
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

env = environ.Env()
env.read_env()

# Create your views here.
@permission_classes([IsAuthenticated])
def rooms(request):
    rooms = User.objects.all()
    return render(request, "room/rooms.html", {"rooms": rooms})

@permission_classes([IsAuthenticated])
def room(request, slug):
    # Get username
    username = request.user.username

    room_name = "{}-{}".format(slug, username)
    reverse_room_name = "{}-{}".format(username, slug)

    # Create the Room if it does not exist
    if not Room.objects.filter(Q(slug=room_name) | Q(slug=reverse_room_name)).exists():
        Room.objects.create(slug=room_name, name=room_name)

    room = Room.objects.get(Q(slug=room_name) | Q(slug=reverse_room_name))
    messages = Message.objects.filter(room=room)[0:25]
    return render(request, "room/room.html", {"room": room, "messages": messages})


class MessagesApi(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer
    def get(self, request, slug):
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


class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ConversationSerializer
    queryset = Room.objects.none()
    lookup_field = "name"

    def get_queryset(self):
        # Getting all active conversations
        queryset = Room.objects.filter(
            name__contains=self.request.user.username
        ).exclude(
            # Exclude conversation with self
            name__contains="{}-{}".format(self.request.user.username, self.request.user.username)    
        )
        return queryset
    
    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}
    
    def retrieve(self, request, name=None):
        user = self.request.user
        room_name = "{}-{}".format(name, user)
        reverse_room_name = "{}-{}".format(user, name)

        room = Room.objects.get(Q(slug=room_name) | Q(slug=reverse_room_name))

        serializer = ConversationSerializer(room, context={"request": request, "user": user})
        return JsonResponse({"room": serializer.data})

class UploadEndpoint(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file = request.FILES['myFile']
        # Save the file to the default storage location
        file_path = default_storage.save(file.name, file)

        # A unique file identifier
        file_identifier = file_path
        print("original file_path", file_path)
        print("original file_identifier", file_identifier)
        # Custom Expiration time (1 day)
        expiration_time = datetime.now() + timedelta(days=1)
        # expiration_time = datetime.now() + timedelta(seconds=10)

        # Return the file location link
        # file_location = default_storage.url(file_path)
        # file_location = default_storage.url(file_path, expiration=expiration_time)

        # If storage method is s3
        if env.bool("USE_S3")==True:
            presigned_url = generate_presigned_url(file_path, expiration_time)

            return JsonResponse({'file_location': presigned_url,
                                'expiration_time': expiration_time.isoformat(),
                                'file_identifier': file_identifier,
                                })
        else:
            # For development only
            return JsonResponse({'file_location': file_path,
                    'expiration_time': None,
                    'file_identifier': file_path,
                    })
    
class RefreshURLView(APIView):
    def get(self, request):
        print("in request.get of refreshurlview")
        message_id = request.GET.get('message_id')
        print("printing message_id: ", message_id)

        # Get the message object from the database
        message_object = Message.objects.get(id=message_id)
        print("message_object: ", message_object.id)
        print("message_object_file_identifier: ", message_object.file_identifier)
        # expiration_time = datetime.now() + timedelta(seconds=10)
        expiration_time = datetime.now() + timedelta(days=1)

        # Generate a new presigned URL with the updated expiration time
        try:
            refreshed_url = generate_presigned_url(message_object.file_identifier, expiration_time)
            print("refreshed_url: ", refreshed_url)
            message_object.multimedia_url = refreshed_url
            message_object.multimedia_url_expiration = expiration_time.isoformat()
            message_object.save()
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'file_location': message_object.multimedia_url})
    
class CheckURLView(APIView):
    def get(self, request):
        message_id = request.GET.get('message_id')
        # Get the message and check if the media url has expired
        message = Message.objects.get(id=message_id)

        # Check if the multimedia link is a local link or an s3 link
        if message.multimedia_save_location == 'local':
            # Does not need refreshing
            return JsonResponse({'refresh_url': False})
    
        elif message.multimedia_save_location == 's3':
            # If its an s3 link keep on checking the other requirements
            if datetime.fromisoformat(message.multimedia_url_expiration) < datetime.now():
                # If the media url has expired, return True
                return JsonResponse({'refresh_url': True})
            else:
                # If the media url has not expired, return False
                print("message.multimedia_url_expiration > datetime.now()")
                return JsonResponse({'refresh_url': False})
        



def generate_presigned_url(file_path, expiration_time):
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
            Params={'Bucket': env("AWS_STORAGE_BUCKET_NAME"), 'Key': file_path},
            ExpiresIn=int((expiration_time - datetime.utcnow()).total_seconds())
        )

        return presigned_url

    except NoCredentialsError as e:
        return JsonResponse({'error': 'AWS credentials not available.'}, status=500)