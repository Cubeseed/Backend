from rest_framework import viewsets
from rest_framework import permissions
from cubeseed.userprofile.serializers import UserProfileSerializer

from cubeseed.userprofile.models import UserProfile

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ['get', 'post', 'patch']
