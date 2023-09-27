from rest_framework import routers
from cubeseed.course import views

def register_routes(router):
    router.register(r"course", views.CourseViewSet)

    return router

urlpatterns = register_routes(routers.DefaultRouter()).urls