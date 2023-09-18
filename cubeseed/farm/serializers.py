from rest_framework import serializers
from geopy.geocoders import Nominatim
from .models import Farm
from .models import Cluster
from .models import Commodity


class FarmSerializerPost(serializers.ModelSerializer):
    """
    Farm serializer for POST requests, it does not include the cluster
    """
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

    
    def create(self, validated_data):
        """
        Overrides the create method to set the cluster_id, if cluster_id is
        not provided in the context, the Farm object is created with a cluster
        set to null by default.
        """
        if self.context:
            cluster_id = self.context["cluster_id"]
            return Farm.objects.create(cluster_id=cluster_id, **validated_data)
        return Farm.objects.create(**validated_data)

class FarmSerializerGet(serializers.ModelSerializer):
    """
    Farm serializer for GET requests, it includes the cluster
    """

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