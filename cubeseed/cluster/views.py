"""Views for Cluster"""
from .models import Cluster
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ClusterSerializer

# Create your views here.
class ClusterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating, editing, and viewing a cluster
    """
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]
