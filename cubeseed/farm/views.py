"""Farm views"""
from rest_framework import viewsets, permissions
from .models import Farm
from .serializers import FarmSerializer


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ["get", "post", "put", "patch"]
