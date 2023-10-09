from rest_framework import serializers
from .models import Message
from cubeseed.userauth.serializers import UserSerializer


class MessageSerializer(serializers.Serializer):
        user = UserSerializer()
        content = serializers.CharField(max_length=2000)
