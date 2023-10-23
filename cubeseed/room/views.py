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
        queryset = Room.objects.filter(
            name__contains=self.request.user.username
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

    


