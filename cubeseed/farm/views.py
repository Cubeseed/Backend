"""Farm views"""
from rest_framework import viewsets, permissions
from .models import Farm
from .serializers import FarmSerializer


class FarmViewSet(viewsets.ModelViewSet):
    # queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ["get", "post", "put", "patch"]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Farm.objects.none()
        if self.kwargs.get('cluster_pk'):
            return Farm.objects.filter(cluster_id=self.kwargs["cluster_pk"])
        return Farm.objects.all()

    def get_serializer_context(self):
        if not getattr(self, 'swagger_fake_view', False):
            if self.kwargs.get('cluster_pk'):
                return {"cluster_id": self.kwargs["cluster_pk"]}

        
