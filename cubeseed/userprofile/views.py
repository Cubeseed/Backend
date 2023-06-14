from rest_framework import viewsets
from rest_framework import permissions
from cubeseed.userprofile.serializers import UserProfilePhotoSerializer, UserProfileSerializer

from cubeseed.userprofile.models import UserProfile

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ['get', 'post', 'put', 'patch']

class UserProfilePhotoViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilePhotoSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ['get', 'post', 'put']
    