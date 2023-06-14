from rest_framework import serializers
from cubeseed.userprofile.models import UserProfile, UserProfilePhoto

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserProfile
        fields = ['url', 'user', 'full_name', 'phone_number', 'address', 'city', 'state', 'country', 'zip_code', 'created_at', 'updated_at' ]
        read_only_fields = [ 'url', 'user', 'created_at', 'updated_at' ]

class UserProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilePhoto
        fields = ['url', 'picture', 'created_at', 'updated_at' ]
        read_only_fields = [ 'url', 'picture', 'created_at', 'updated_at' ]