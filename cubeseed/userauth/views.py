from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from cubeseed.userauth.serializers import UserSerializer, GroupSerializer, RegisterUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ["get"]


class RegisterUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ["post"]
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer
