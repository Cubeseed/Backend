from rest_framework import serializers
from geopy.geocoders import Nominatim
from .models import Farm
from .models import Cluster
from .models import Commodity


class FarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = [
            "id",
            "business_profile",
            "name",
            "size",
            "commodity",
            "farm_address",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    # Override the create method to set the cluster_id
    def create(self, validated_data):
        if self.context:
            cluster_id = self.context["cluster_id"]
            return Farm.objects.create(cluster_id=cluster_id, **validated_data)
        return Farm.objects.create(**validated_data)
    

class AssignFarmToClusterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = [
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    # Custom function to assign a farm to a cluster
    def assign_farm_to_cluster(self, farm_id):
        # Get the farm
        farm = Farm.objects.get(id=farm_id)

        # Get the address (longitude and latitude)
        osm_longitude = farm.farm_address.osm_longitude
        osm_latitude = farm.farm_address.osm_latitude

        # Retrieve farm county
        geolocator = Nominatim(user_agent="cubeseed-backend")
        location = geolocator.reverse("{}, {}".format(osm_latitude, osm_longitude))

        # county is equivalent to LGA
        farm_local_government_name = location.raw["address"]["county"]
        farm_local_government_name = "Aba North"

        # Get Commodity produced in the farm
        farm_commodity = farm.commodity.id

        # Check if a cluster that produces the commodity
        # exists with in that local government area / county
        try:
            cluster = Cluster.objects.get(local_government_name=farm_local_government_name, commodity=farm_commodity)
            # If yes, assign that farm to the cluster
            farm.cluster = cluster
            farm.save()
            return farm
        except Exception as e:
            # If no, create the cluster and assign the farm to the cluster
            # Creating the cluster
            new_cluster = Cluster()
            new_cluster.cluster_name = "{} {} cluster".format(farm_local_government_name, farm_commodity)
            new_cluster.local_government_name = farm_local_government_name
            # Get Commodity object
            farm_commodity_object = Commodity.objects.get(id = farm_commodity)
            new_cluster.commodity = farm_commodity_object
            new_cluster.save()

            # Assigning the farm to the cluster
            farm.cluster = new_cluster
            farm.save()
            return farm

    # Override the create method to set the cluster_id
    def create(self, validated_data):
        farm_id = self.context["farm_id"]
        farm = self.assign_farm_to_cluster(farm_id)
        return farm