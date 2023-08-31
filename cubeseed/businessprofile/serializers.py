from rest_framework import serializers
from .models import BusinessProfile


class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BusinessProfile
        fields = "__all__"
        read_only_fields = ["url", "user", "created_at", "updated_at"]
