from rest_framework import serializers
from .models import PurchaseOrder, OpenedPurchaseOrder

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class OpendPurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenedPurchaseOrder
        fields = '__all__'
