from rest_framework import viewsets, permissions
from .models import courseVerification
from .serializer import CourseVerificationSerializer


class CourseVerificationViewSet(viewsets.ModelViewSet):
    queryset = courseVerification.objects.all()
    serializer_class = CourseVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch"]