from rest_framework import routers
from cubeseed.commodity import views

def register_router(router):
    router.register(r"commodity", views.CommodityViewSet)
    return router

urlpatterns = register_router(routers.DefaultRouter()).urls