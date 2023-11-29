from rest_framework import serializers
from .models import Message
from cubeseed.userauth.serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import Room
import environ

env = environ.Env()
env.read_env()

class MessageSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        from_user = UserSerializer()
        to_user = UserSerializer()
        date_added = serializers.DateTimeField()
        content = serializers.CharField(max_length=2000)
        # multimedia_save_location = serializers.CharField(max_length=2000, allow_blank=True, allow_null=True)
        # multimedia_url = serializers.CharField(max_length=2000, allow_blank=True, allow_null=True)
        multimedia_url = serializers.SerializerMethodField()

        def get_multimedia_url(self, obj):
                # if multimedia is stored locally
                # modify the url
                if obj.multimedia_save_location == 'local':
                        multimedia_url = self.generate_working_link_for_local_multimedia(obj.multimedia_url)
                        return multimedia_url
                else:
                        return obj.multimedia_url

                # else
        # For development purposes only
        def generate_working_link_for_local_multimedia(self, multimedia_url):
                # Generating a working link for the multimedia_url if it is a local link
                multimedia_url = "http://{}:{}/chat-media/".format(env("HOST"), env("PORT")) + multimedia_url
                return multimedia_url

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