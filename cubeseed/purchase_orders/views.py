from rest_framework import viewsets, permissions
from .models import PurchaseOrder, OpenedPurchaseOrder
from .serializer import PurchaseOrderSerializer, OpendPurchaseOrderSerializer

class PurchasedOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]

class OpenedPurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = OpenedPurchaseOrder.objects.all()
    serializer_class = OpendPurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]
