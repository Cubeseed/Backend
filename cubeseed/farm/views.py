"""Farm views"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from geopy.geocoders import Nominatim
from django.http import HttpResponse
from .models import Farm, Cluster, Commodity
from .serializers import FarmSerializerGet, FarmSerializerPost


class FarmViewSet(viewsets.ModelViewSet):
    """
    ViewSet for creating, editing, and viewing a farm
    """
    serializer_class_post = FarmSerializerPost
    serializer_class_get = FarmSerializerGet
    permission_classes = [permissions.DjangoModelPermissions]
    http_method_names = ["get", "post", "put", "patch"]

    def get_serializer_class(self):
        """
        Provides a different serializer class for different
        request methods
        """
        if self.request.method == 'POST':
            return self.serializer_class_post
        elif self.request.method == 'GET':
            return self.serializer_class_get

    def get_queryset(self):
        """
        A custom implementation of the get_queryset method that checks if 
        a cluster_pk is provided as a keyword argument and returns a queryset 
        of farms filtered by the cluster_pk. If no cluster_pk is provided, all
        farms are returned.

        Returns: 
        Farm QuerySet
            A queryset of farms filtered by the cluster_pk or all farms or None
        """
        # If the view is called from the swagger UI, return an empty queryset
        # this will avoid error related to cluster_pk not being provided
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Farm.objects.none()
        if self.kwargs.get('cluster_pk'):
            return Farm.objects.filter(cluster_id=self.kwargs["cluster_pk"])
        return Farm.objects.all()

    def get_serializer_context(self):
        """
        Passes a context dictionary that contains the cluster_id to the serializer class,
        to be used in the create method

        Returns: 
        Dictionary
            A dictionary containing the cluster_id
        """
        if not getattr(self, 'swagger_fake_view', False):
            if self.kwargs.get('cluster_pk'):
                return {"cluster_id": self.kwargs["cluster_pk"]}
    
    @staticmethod
    def extract_lga_of_farm(farm):
        """
        Given a farm object, this method extracts the LGA of the farm
        using the longitude and latitude of the farm.
        
        Parameters: 
        farm: Farm
            A farm object 
        
        Returns: 
        String or None
            Returns the LGA name or None if the LGA could not be extracted
        """
        # Get the address (longitude and latitude)
        osm_longitude = farm.farm_address.osm_longitude
        osm_latitude = farm.farm_address.osm_latitude

        # Retrieve farm lga/county
        geolocator = Nominatim(user_agent="cubeseed-backend")
        location = geolocator.reverse("{}, {}".format(osm_latitude, osm_longitude))

        try:
            farm_local_government_name = location.raw["address"]["county"]
            return farm_local_government_name
        except Exception:
            # If the LGA could not be extracted, return None
            return None
    
    @staticmethod
    def check_if_cluster_exists(farm_local_government_name, farm_commodity):
        """
        Checks if a cluster that produces the commodity within in that LGA/country exists
        Parameters: String, Commodity

        Parameters:
        farm_local_government_name: String
            The name of the local government area or county of the farm
        farm_commodity: Commodity
            The commodity produced in the farm

        Returns:
        Cluster or None
            Returns the cluster object if it exists or None if it does not exist
        """
        try:
            cluster = Cluster.objects.get(local_government_name=farm_local_government_name, commodity=farm_commodity)
            return cluster
        except Cluster.DoesNotExist:
            return None
        
    @staticmethod
    def create_new_cluster(farm_local_government_name, farm_commodity):
        """
        Creates a new cluster
        
        Parameters: 
        String, Commodity
            farm_local_government_name: String
                The name of the local government area or county of the farm
            farm_commodity: Commodity
                The commodity produced in the farm

        Returns:
        Cluster
            Returns the cluster object 
        """
        cluster_name = "{} {} cluster".format(farm_local_government_name, farm_commodity.commodity_name)
        # commodity_object = Commodity.objects.get(id=farm_commodity)
        cluster = Cluster.objects.create(cluster_name=cluster_name, local_government_name=farm_local_government_name, commodity=farm_commodity)
        return cluster
    
    @action(detail=True)
    def cluster(self, request, pk=None):
        """
        Custom action that will be called when the endpoint /farms/{pk}/cluster is called

        Returns:
        HttpResponse
            Returns an HttpResponse with a status code of 200 if the farm is successfully assigned to a cluster
        """
        if not getattr(self, 'swagger_fake_view', False):
            # Get the farm
            farm_id = self.kwargs.get('pk')
            farm = Farm.objects.get(id=farm_id)

            # Retrieve the LGA name or County of the farm
            farm_local_government_name = self.extract_lga_of_farm(farm)
            
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

