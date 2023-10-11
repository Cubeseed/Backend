from rest_framework import serializers
from .models import FarmPlanner


class FarmPlannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmPlanner
        fields = ["farmer", "purchase_order", "short_description", "order_tracker", "order_status", "timestamp"]

    # serialize time stamp field to a readable format
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["timestamp"] = instance.timestamp.strftime("%d %b %Y %H:%M")
        return data
