from rest_framework import viewsets, permissions
from .models import CourseVerification
from .serializer import CourseVerificationSerializer


class CourseVerificationViewSet(viewsets.ModelViewSet):
    queryset = CourseVerification.objects.all()
    serializer_class = CourseVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch"]