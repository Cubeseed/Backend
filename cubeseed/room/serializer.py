from rest_framework import serializers
from .models import Message
from cubeseed.userauth.serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import Room

class MessageSerializer(serializers.Serializer):
        from_user = UserSerializer()
        to_user = UserSerializer()
        date_added = serializers.DateTimeField()
        content = serializers.CharField(max_length=2000)

User = get_user_model()

class ConversationSerializer(serializers.ModelSerializer):
        other_user = serializers.SerializerMethodField()
        last_message = serializers.SerializerMethodField()

        class Meta:
                model = Room
                fields = ("id", "name", "other_user", "last_message")

        def get_last_message(self, obj):
                messages = obj.messages.all().order_by("-date_added")
                if not messages.exists():
                        return None
                message = messages[0]
                return MessageSerializer(message, context=self.context).data
        
        def get_other_user(self, obj):
                usernames = obj.name.split("-")
                context = {}
                for username in usernames:
                        if username != self.context['user'].username:
                                # This is the other participant
                                other_user = User.objects.get(username=username)
                                return UserSerializer(other_user, context=self.context).data