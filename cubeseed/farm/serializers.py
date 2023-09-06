from rest_framework import serializers
from .models import Farm


class FarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = [
            "id",
            "business_profile",
            "name",
            "size",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    # Override the create method to set the cluster_id
    def create(self, validated_data):
        if self.context:
            cluster_id = self.context["cluster_id"]
            return Farm.objects.create(cluster_id=cluster_id, **validated_data)
        return Farm.objects.create(**validated_data)