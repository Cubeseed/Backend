from rest_framework import serializers
from .models import Commodity

class CommoditySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Commodity
        fields = "__all__"