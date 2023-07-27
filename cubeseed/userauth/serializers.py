from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers

from Backend.cubeseed.userauth.models import Course


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
        serializer for fetching users
    """
    class Meta:
        model = get_user_model()
        fields = ["url", "username", "email", "groups", "is_active"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
        serializer for creating user group
    """
    class Meta:
        model = Group
        fields = ["url", "name"]


class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):
    """
        serializer for creating a new user
    """
    class Meta:
        model = get_user_model()
        fields = ["url", "username", "email", "groups", "password", "is_active"]
        read_only_fields = ["url", "is_active"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False,
        )
        user.groups.set(validated_data["groups"])
        user.save()
        return user

    class CourseSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Course
            fields = ['link', 'title', 'description', 'date_created', 'updated']

        def create(self, validated_data):
            course = Course.objects.create_user(
                link=validated_data["link"],
                title=validated_data["username"],
                description=validated_data['description'],
                date_created=validated_data["date_created"],
                updated=validated_data["updated"],
            )
            course.save()
            return course
