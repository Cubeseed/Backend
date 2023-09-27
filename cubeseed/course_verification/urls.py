from rest_framework import routers
from cubeseed.course_verification import views

def register_routes(router):
    router.register(r"course_verification", views.CourseVerificationViewSet)

    return router

urlpatterns = register_routes(routers.DefaultRouter()).urls