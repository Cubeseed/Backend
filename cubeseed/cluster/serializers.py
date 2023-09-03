from rest_framework import serializers
from .models import Cluster

class ClusterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cluster
        fields = "__all__"