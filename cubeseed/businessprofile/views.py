"""Business profile views"""
from rest_framework import viewsets, permissions
from .models import BusinessProfile
from .serializers import BusinessProfileSerializer


class BusinessProfileViewSet(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    #permission_classes = [permissions.DjangoModelPermissions]
    permissions_class = [permissions.IsAuthenticated] # Enable me For testing only!!
    http_method_names = ["get", "post", "put", "patch"]
