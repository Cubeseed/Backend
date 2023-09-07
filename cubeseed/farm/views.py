"""Farm views"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from geopy.geocoders import Nominatim
from django.http import HttpResponse
from .models import Farm, Cluster, Commodity
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
    
    @staticmethod
    def extract_lga_of_farm(farm):
        # Get the address (longitude and latitude)
        osm_longitude = farm.farm_address.osm_longitude
        osm_latitude = farm.farm_address.osm_latitude

        # Retrieve farm county
        geolocator = Nominatim(user_agent="cubeseed-backend")
        location = geolocator.reverse("{}, {}".format(osm_latitude, osm_longitude))

        # county is equivalent to LGA
        try:
            farm_local_government_name = location.raw["address"]["county"]
            return farm_local_government_name
        except Exception:
            return None
    
    @staticmethod
    def check_if_cluster_exists(farm_local_government_name, farm_commodity):
        try:
            cluster = Cluster.objects.get(local_government_name=farm_local_government_name, commodity=farm_commodity)
            return cluster
        except Cluster.DoesNotExist:
            return None
        
    @staticmethod
    def create_new_cluster(farm_local_government_name, farm_commodity):
        cluster_name = "{} {} cluster".format(farm_local_government_name, farm_commodity.commodity_name)
        # commodity_object = Commodity.objects.get(id=farm_commodity)
        cluster = Cluster.objects.create(cluster_name=cluster_name, local_government_name=farm_local_government_name, commodity=farm_commodity)
        return cluster
    
    @action(detail=True)
    def cluster(self, request, pk=None):
        if not getattr(self, 'swagger_fake_view', False):
            # Get the farm
            farm_id = self.kwargs.get('pk')
            farm = Farm.objects.get(id=farm_id)

        # Retrieve the LGA name or County of the farm
        # farm_local_government_name = self.extract_lga_of_farm(farm)
        farm_local_government_name = "Aba North"
        if farm_local_government_name is None:
            return HttpResponse("LGA of farm could not be extracted", status=400)

        # Get Commodity produced in the farm
        farm_commodity = farm.commodity

        # Check if a cluster that produces the commodity
        # exists with in that local government area / county
        cluster = self.check_if_cluster_exists(farm_local_government_name, farm_commodity)
        if cluster:
            # If yes, assign that farm to the cluster
            farm.cluster = cluster
            farm.save()
            return HttpResponse("Farm successfully assigned to cluster", status=200)
        else:
            # Create a new cluster
            cluster = self.create_new_cluster(farm_local_government_name, farm_commodity)
            # Assign the farm to the cluster
            farm.cluster = cluster
            farm.save()
            return HttpResponse("Farm successfully assigned to cluster", status=200)

