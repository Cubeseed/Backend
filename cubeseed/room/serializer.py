from rest_framework import serializers
from .models import Message
from cubeseed.userauth.serializers import UserSerializer


class MessageSerializer(serializers.Serializer):
        from_user = UserSerializer()
        to_user = UserSerializer()
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