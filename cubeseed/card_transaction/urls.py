from rest_framework.routers import DefaultRouter
from .views import PaymentCardViewSet, CardTransactionViewSet, PaymentGatewayViewSet, TransactionViewSet

def register_routes(router):
    router.register(r"payment-cards", PaymentCardViewSet)
    router.register(r"card-transactions", CardTransactionViewSet)
    router.register(r"payment-gateways", PaymentGatewayViewSet)
    router.register(r"transactions", TransactionViewSet)

    return router

url_patterns = register_routes(DefaultRouter()).urls
