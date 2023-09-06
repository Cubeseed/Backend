from rest_framework import routers
# from rest_framework_nested import routers as drf_nested_routers
from cubeseed.cluster import views

def register_routes(router):
    router.register(r"cluster", views.ClusterViewSet)
    return router

urlpatterns = register_routes(routers.DefaultRouter()).urls