from rest_framework import routers
from cubeseed.businessprofile import views

def register_routes(router):
    router.register(r"businessprofile", views.BusinessProfileViewSet)

    return router

urlpatters = register_routes(routers.DefaultRouter()).urls