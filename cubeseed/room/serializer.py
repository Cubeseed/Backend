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

# class MessageSerializer(serializers.ModelSerializer):
#     from_user = serializers.SerializerMethodField()
#     to_user = serializers.SerializerMethodField()
#     room = serializers.SerializerMethodField()

#     class Meta:
#         model = Message
#         fields = (
#             "id",
#             "room",
#             "from_user",
#             "to_user",
#             "content",
#             "date_added",
#             "read",
#         )

#     def get_room(self, obj):
#         return str(obj.room.id)
    
#     def get_from_user(self, obj):
#         return UserSerializer(obj.from_user).data
    
#     def get_to_user(self, obj):
#         return UserSerializer(obj.to_user).data

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
                                print("Printing other user: ", other_user)
                                # return UserSerializer(other_user, context=context).data
                                return UserSerializer(other_user, context=self.context).data