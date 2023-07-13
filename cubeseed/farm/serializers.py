from rest_framework import serializers
from .models import Farm


class FarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = [
            "url",
            "business_profile",
            "name",
            "size",
        ]
        read_only_fields = ["url", "user", "created_at", "updated_at"]
