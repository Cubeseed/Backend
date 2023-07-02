from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups", "is_active"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups", "password", "is_active"]
        read_only_fields = ["url", "is_active"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False,
        )
        user.groups.set(validated_data["groups"])
        user.save()
        return user
