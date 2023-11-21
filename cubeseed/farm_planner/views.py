from rest_framework import viewsets, permissions
from .models import FarmPlanner
from .serializer import FarmPlannerSerializer


class FarmPlannerViewSet(viewsets.ModelViewSet):
    queryset = FarmPlanner.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FarmPlannerSerializer

    # override the get queryset method to get only the  PO of the current user
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return self.objects.none()
        user = self.request.user
        return FarmPlanner.objects.filter(farmer=user)