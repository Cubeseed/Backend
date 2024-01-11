"""Room Serializers"""
from rest_framework import serializers
from .models import Message
from cubeseed.userauth.serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import Room
import environ

env = environ.Env()
env.read_env()

class MessageSerializer(serializers.Serializer):
        """
        Messsage Serializer
        """
        id = serializers.IntegerField(read_only=True)
        from_user = UserSerializer()
        to_user = UserSerializer()
        date_added = serializers.DateTimeField()
        content = serializers.CharField(max_length=2000)

        def get_multimedia_url(self, obj):
                """
                Custom method that gets the multimedia url
                If the multimedia is stored locally, it generates 
                a working link and returns the link.
                If the multimedia is not stored locally, it returns 
                the multimedia_url.

                Parameters:
                obj: Message
                    The message object

                Returns:
                String
                    The multimedia url
                """
                # If multimedia is stored locally generate a working
                # link
                if obj.multimedia_save_location == 'local':
                        multimedia_url = self.generate_working_link_for_local_multimedia(obj.multimedia_url)
                        return multimedia_url
                else:
                        return obj.multimedia_url

        # For development purposes only
        def generate_working_link_for_local_multimedia(self, multimedia_url):
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
        
        def to_representation(self, obj):
                """
                Overides the to_representation method to add the multimedia_url
                to the serialized representation if it is not None

                Parameters:
                obj: Message
                        The message object to be serialized

                Returns:
                OrderedDict
                        The serialized represenation
                """
                ret = super().to_representation(obj)
                # Check if multimedia_url is not None before adding it to the representation
                if obj.multimedia_url:
                        import pdb
                        pdb.set_trace()
                        ret['multimedia_url'] = self.get_multimedia_url(obj)
                return ret

User = get_user_model()

class ConversationSerializer(serializers.ModelSerializer):
        """
        Serializer for the Room model, representing a conversation between users.
        Includes additional fields for the other participant in the conversation 
        and the last message sent.
        """
        other_user = serializers.SerializerMethodField()
        last_message = serializers.SerializerMethodField()

        class Meta:
                model = Room
                fields = ("id", "name", "other_user", "last_message")

        def get_last_message(self, obj):
                """
                Retrieves the last message sent in the conversation.

                Parameters:
                obj: Room
                        The Room instance being serialized.

                Returns:
                Dict or None
                        Returns the serialized data of the last message, or None if no messages exist.
                """
                messages = obj.messages.all().order_by("-date_added")
                if not messages.exists():
                        return None
                message = messages[0]
                return MessageSerializer(message, context=self.context).data
        
        def get_other_user(self, obj):
                """
                Retrieves the other participant in the conversation.

                Parameters:
                obj: Room
                        The Room instance being serialized.

                Returns:
                Dict
                        Returns the serialized data of the other user.
                """
                usernames = obj.name.split("-")
                context = {}
                for username in usernames:
                        if username != self.context['user'].username:
                                # This is the other participant
                                other_user = User.objects.get(username=username)
                                return UserSerializer(other_user, context=self.context).data