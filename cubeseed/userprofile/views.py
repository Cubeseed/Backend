import os
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
import magic
from cubeseed.userprofile.serializers import UserProfilePhotoSerializer, UserProfileSerializer
from cubeseed.userprofile.models import UserProfile, UserProfilePhoto


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ["get", "post", "put", "patch"]


class UserProfilePhotoViewSet(viewsets.ModelViewSet):
    queryset = UserProfilePhoto.objects.all()
    serializer_class = UserProfilePhotoSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ["get", "post", "patch", "put", "delete"]

    def retrieve(self, request, *args, **kwargs):
        user_profile_photo = self.get_object()
        if user_profile_photo.picture:
            buffer = open(user_profile_photo.picture.path, "rb").read()
            content_type = magic.from_buffer(buffer, mime=True)
            response = HttpResponse(buffer, content_type=content_type)
            response[
                "Content-Disposition"
            ] = f'attachment; filename="{os.path.basename(user_profile_photo.picture.path)}"'
            return response
        else:
            return super().retrieve(request, *args, **kwargs)
