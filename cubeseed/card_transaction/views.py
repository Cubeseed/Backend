from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import PaymentCard, CardTransaction, PaymentGateway, Transaction
from .serializer import PaymentCardSerializer, CardTransactionSerializer, PaymentGatewaySerializer, TransactionSerializer



class PaymentCardViewSet(viewsets.ModelViewSet):
    queryset = PaymentCard.objects.all()
    serializer_class = PaymentCardSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]

    # custom action to call the validation function from POST request
    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        card = self.get_object()
        print(card)

        try:
            card.validate_card()
            return Response({"detail": "Card is valid"}, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response({"detail": error.message}, status=status.HTTP_400_BAD_REQUEST)

    # custom action to call the encryption function from POST request
    @action(detail=True, methods=['post'])
    def encrypt(self, request, pk=None):
        card = self.get_object()

        try:
            card.encrypt_card()
            return Response({"detail": "Card details encrypted successfully"}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)


class CardTransactionViewSet(viewsets.ModelViewSet):
    queryset = CardTransaction.objects.all()
    serializer_class = CardTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]

class PaymentGatewayViewSet(viewsets.ModelViewSet):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]
