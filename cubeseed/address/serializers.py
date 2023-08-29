from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "url",
            "address",
            "address_detail",
            "locality",
            "administrative_area",
            "country",
            "postal_code",
            "osm_checked",
            "osm_longitude",
            "osm_latitude",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["url", "osm_checked", "osm_longitude", "osm_latitude", "created_at", "updated_at"]
