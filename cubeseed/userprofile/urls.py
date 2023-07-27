from rest_framework import routers
from cubeseed.userprofile import views


def register_routes(router):
    router.register(r"userprofile", views.UserProfileViewSet)
    router.register(r"userprofilephoto", views.UserProfilePhotoViewSet)
    router.register(r"courseverification", views.CourseVerification)
    return router


urlpatterns = register_routes(routers.DefaultRouter()).urls
