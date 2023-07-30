from rest_framework import serializers
from cubeseed.userprofile.models import UserProfile, UserProfilePhoto, FarmerProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserProfile
        fields = [
            "url",
            "user",
            "full_name",
            "phone_number",
            "address",
            "city",
            "state",
            "country",
            "zip_code",
            "about_me",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["url", "user", "created_at", "updated_at"]


class UserProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilePhoto
        fields = ["url", "user_profile", "picture", "created_at", "updated_at"]
        read_only_fields = ["url", "created_at", "updated_at"]
        extra_kwargs = {"picture": {"write_only": True}}


class FarmerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = FarmerProfile
        fields = ["user_profile", "review_status"]