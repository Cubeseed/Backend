from rest_framework import viewsets
from rest_framework import permissions

from cubeseed.filedescriptor.serializers import CourseCertificateFileSerializer
from cubeseed.filedescriptor.models import CourseCertificateFile

class CourseCertificateFileViewSet(viewsets.ModelViewSet):
    queryset = CourseCertificateFile.objects.all()
    serializer_class = CourseCertificateFileSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ["get", "post", "put", "patch"]
