from rest_framework import routers
from cubeseed.userprofile import views

def register_routes(router):
    router.register(r'userprofile', views.UserProfileViewSet)
    router.register(r'userprofile/photo', views.UserProfilePhotoViewSet)
    return router

urlpatterns = register_routes(routers.DefaultRouter()).urls
