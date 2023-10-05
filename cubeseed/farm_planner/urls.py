from rest_framework.routers import DefaultRouter
from cubeseed.farm_planner import views


def register_routes(router):
    router.register(r"farm-planner", views.FarmPlannerViewSet)

    return router

url_patterns = register_routes(DefaultRouter()).urls
