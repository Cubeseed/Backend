from rest_framework import routers
from cubeseed.commodity import views

def register_routes(router):
    router.register(r"commodity", views.CommodityViewSet)
    return router

urlpatterns = register_routes(routers.DefaultRouter()).urls