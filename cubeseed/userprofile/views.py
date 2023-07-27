import os
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework import permissions
import magic
from rest_framework.decorators import api_view
from rest_framework.response import Response
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


class CourseVerification(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ["get", "post"]

    @api_view(['POST'])
    def verify_user(request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            assigned_code = serializer.validated_data['assigned_code']
            upload_certificate = serializer.validated_data['upload_certificate']

            try:
                user_profile = UserProfile.objects.get(
                    assigned_code=assigned_code,
                )
                user_profile.upload_certificate = upload_certificate
                user_profile.save()

                return Response({'message': 'User verified and upload_certificate uploaded successfully.'},
                                status=status.HTTP_200_OK)
            except UserProfile.DoesNotExist:
                return Response({'message': 'User verification failed. Invalid code or details,try agan.'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
