from rest_framework import serializers
from .models import Invoice, Waybill, Receipt


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class WaybillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waybill
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'
