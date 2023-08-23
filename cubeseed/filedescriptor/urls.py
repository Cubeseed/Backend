from rest_framework import routers
from cubeseed.filedescriptor import views


def register_routes(router):
    router.register(r"coursecertificate", views.CourseCertificateFileViewSet)
    return router

urlpatterns = register_routes(routers.DefaultRouter()).urls