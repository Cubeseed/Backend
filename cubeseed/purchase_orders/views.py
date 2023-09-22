from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PurchaseOrder, OpenedPurchaseOrder
from .serializer import PurchaseOrderSerializer, OpendPurchaseOrderSerializer


class PurchasedOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]

    # custom action to accept a purchase order
    @action(detail=True, methods=["post"])
    def accept_order(self, request, pk=None):
        purchase_order = self.get_object()

        # check if the purchase order has already been accepted/bought by other person
        if purchase_order.accepted_by is not None:
            return Response({"detail": "This purchase order is already accepted."}, status=status.HTTP_400_BAD_REQUEST)

        # update the purchase order's accepted_by field to the current user
        purchase_order.accepted_by = request.user
        purchase_order.save()

        # Create an openedPurchaseOrder object entery for the accepted order
        opened_purchase_order = OpenedPurchaseOrder.objects.create(purchase_order=purchase_order, farmer=request.user)
        opened_purchase_order.save()

        # Serialize the updated purchase order and return the response
        serializer = self.get_serializer(purchase_order)
        return Response(serializer.data)

class OpenedPurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = OpenedPurchaseOrder.objects.all()
    serializer_class = OpendPurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]
