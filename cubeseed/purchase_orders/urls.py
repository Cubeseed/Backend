from rest_framework.routers import DefaultRouter
from .views import PurchasedOrderViewSet, OpenedPurchaseOrderViewSet

def register_routes(router):
    router.register(r"purchase-orders", PurchasedOrderViewSet)
    router.register(r"opened-purchase-orders", OpenedPurchaseOrderViewSet)

    return router

url_patterns = register_routes(DefaultRouter()).urls
