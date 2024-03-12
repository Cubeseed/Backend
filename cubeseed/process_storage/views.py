from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProcessStorage, DispatchedStorage
from .serializer import ProcessStorageSerializer, DispatchedStorageSerializer


class ProcessStorageViewSet(viewsets.ModelViewSet):
    queryset = ProcessStorage.objects.all()
    serializer_class = ProcessStorageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]

    # @action(detail=True, methods=["post"])
    # def dispatch(self, request, pk=None):
    #     process_storage = self.get_object()

    #     serializer = self.get_serializer(process_storage, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class DispatchedStorageViewSet(viewsets.ModelViewSet):
    queryset = DispatchedStorage.objects.all()
    serializer_class = DispatchedStorageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]
