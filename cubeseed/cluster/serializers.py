from rest_framework import serializers
from .models import Cluster
from cubeseed.farm.serializers import FarmSerializerGet

class ClusterSerializer(serializers.ModelSerializer):
    farms = FarmSerializerGet(many=True, read_only=True)
    class Meta:
        model = Cluster
        fields = [
            'id',
            'cluster_name', 
            'local_government_name', 
            'commodity', 
            'farms',
        ]