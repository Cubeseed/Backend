from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, WaybillViewSet, ReceiptViewSet

def register_routes(router):
    router.register(r"invoice", InvoiceViewSet)
    router.register(r"waybill", WaybillViewSet)
    router.register(r"receipt", ReceiptViewSet)

    return router

url_patterns = register_routes(DefaultRouter()).urls
