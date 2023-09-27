from rest_framework import viewsets, permissions
from .models import Course
from .serializer import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permissions_class = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch"]