from rest_framework import serializers
from geopy.geocoders import Nominatim
from .models import Farm
from .models import Cluster
from .models import Commodity


class FarmSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = [
            "id",
            "business_profile",
            "name",
            "size",
            "commodity",
            "farm_address",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    # Override the create method to set the cluster_id
    def create(self, validated_data):
        if self.context:
            cluster_id = self.context["cluster_id"]
            return Farm.objects.create(cluster_id=cluster_id, **validated_data)
        return Farm.objects.create(**validated_data)

class FarmSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = [
            "id",
            "business_profile",
            "name",
            "size",
            "commodity",
            "farm_address",
            "cluster",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]