from rest_framework import serializers
from .models import Commodity

class CommoditySerializer(serializers.ModelSerializer):
    """
    Serializer for Commodity
    """
    class Meta:
        model = Commodity
        fields = "__all__"