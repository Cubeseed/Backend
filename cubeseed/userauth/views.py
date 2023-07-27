from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from cubeseed.userauth.serializers import UserSerializer, GroupSerializer, RegisterUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get"]


class RegisterUserView(viewsets.ModelViewSet):
    """
    API endpoint that registers a user.
    """

    queryset = get_user_model().objects.all()
    http_method_names = ["post"]
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer
