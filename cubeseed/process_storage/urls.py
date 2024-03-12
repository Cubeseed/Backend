from rest_framework.routers import DefaultRouter
from .views import ProcessStorageViewSet, DispatchedStorageViewSet

def register_routes(router):
    router.register(r"process-storage", ProcessStorageViewSet)
    router.register(r"dispatch-storage", DispatchedStorageViewSet)

    return router

url_patterns = register_routes(DefaultRouter()).urls