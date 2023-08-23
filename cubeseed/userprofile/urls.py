from rest_framework import routers
from cubeseed.userprofile import views
from cubeseed.farm import views 


def register_routes(router):
    router.register(r"userprofile", views.UserProfileViewSet)
    router.register(r"userprofilephoto", views.UserProfilePhotoViewSet)
    router.register(r"farmerprofile", views.FarmerProfileViewSet)
    return router


urlpatterns = register_routes(routers.DefaultRouter()).urls
