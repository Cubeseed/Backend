"""Views for Commodity"""
from .models import Commodity
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CommoditySerializer
# Create your views here.


class CommodityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating, editing, and viewing a commodity
    """
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]
