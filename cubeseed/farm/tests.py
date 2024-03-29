from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from cubeseed.commodity.models import Commodity
from cubeseed.address.models import Address
from cubeseed.businessprofile.models import BusinessProfile
from cubeseed.cluster.models import Cluster
from rest_framework import status
from .models import Farm
from unittest.mock import Mock
from unittest.mock import patch

# Create a Mock of the resolve_location function
# found in the Address Model.
# This prevents the geocode function from being 
# called multiple times.
mock_resolve_location = Mock()

def side_effect(address):
    class Location:
        def __init__(self, latitude, longitude):
            self.longitude = longitude
            self.latitude = latitude
    if address == "979 Saka Jojo Street, Victoria, Lagos, ":
        location = Location(6.4275875, 3.4126698)
        return location
    elif address == "2 Walter Carrington Crescent, Victoria Island, Lagos, ":
        location = Location(6.44069015, 3.4066570357293076)
        return location
    elif address == "1075 Diplomatic Drive, Central District Area, Abuja, 900103":
        location = Location(9.0403859, 7.4768889)
        return location
    else:
        return None

# Create your tests here.
User = get_user_model()
class FarmAPITest(APITestCase):

    @patch.object(Address, "resolve_location", side_effect=side_effect)
    def setUp(self, mock_resolve_location) -> None:
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user.is_active = True
        self.user.groups.add(Group.objects.get(name="farmer"))
        self.user.save()
        self.url = reverse("user-detail", kwargs={"pk": self.user.pk})

        # Create Commodities
        self.commodity_maize = Commodity.objects.create(commodity_name="Maize")
        self.commodity_maize.save()

        self.commodity_cassava = Commodity.objects.create(commodity_name="Cassava")
        self.commodity_cassava.save()
        
        # Create Address
        self.address_eti_osa = Address.objects.create(
                address="979 Saka Jojo Street",
                address_detail="",
                locality="Victoria",
                administrative_area="Lagos",
                country="NG",
                postal_code="",
                local_government_area="Eti Osa",
        )
        self.address_eti_osa.save()

        # Create Address 2
        self.address_eti_osa_2 = Address.objects.create(
            address="2 Walter Carrington Crescent",
            address_detail="",
            locality="Victoria Island",
            administrative_area="Lagos",
            country="NG",
            postal_code="",
            local_government_area="Eti Osa",
        )
        self.address_eti_osa_2.save()

        # Create Address 3
        self.address_municipal_area_council = Address.objects.create(
            address="1075 Diplomatic Drive",
            address_detail="",
            locality="Central District Area",
            administrative_area="Abuja",
            country="NG",
            postal_code="900103",
            local_government_area="Municipal Area Council",  
        )

        self.address_municipal_area_council.save()

        # Create business profile
        self.samuels_business_profile = BusinessProfile.objects.create(
            user=self.user,
            business_name="Samuels Business",
            email="samuel@example.com",
            telephone="1234",
            billing_address="979 Saka Jojo Street",
            shipping_address="979 Saka Jojo Street",
            logo="null",
            document_type="TIN",
        )
        self.samuels_business_profile.save()


        # Create business profile 2
        self.peters_business_profile = BusinessProfile.objects.create(
            user=self.user,
            business_name="Peters Business",
            email="peter@example.com",
            telephone="1234",
            billing_address="2 Walter Carrington Crescent",
            shipping_address="2 Walter Carrington Crescent",
            logo="null",
            document_type="TIN",
        )
        self.peters_business_profile.save()

        # Create business profile 3
        self.johns_business_profile = BusinessProfile.objects.create(
            user=self.user,
            business_name="Johns Business",
            email="john@example.com",
            telephone="1234",
            billing_address="1075 Diplomatic Drive",
            shipping_address="1075 Diplomatic Drive",
            logo="null",
            document_type="TIN",
        )
        self.johns_business_profile.save()
    
        # Create Farm
        self.farm = Farm.objects.create(
            business_profile=self.johns_business_profile,
            name="Johns Municipal Area Council Maize Farm",
            size="10",
            commodity=self.commodity_maize,
            farm_address=self.address_municipal_area_council
        )
        self.farm.save()

    def authenticate(self):
        token_response = self.client.post(
            reverse("token_obtain_pair"), {"username": "testuser", "password": "testpassword"}
        )
        access_token = token_response.data["access"]
        # refresh_token = token_response.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")


    # Test if a farm can be created successfully
    # using an authenticated and authorized user
    def test_successful_farm_creation_using_authenticated_and_authorized_user(self):
        """
        Tests that farms can be created
        successfully using an authenticated
        and authorized user
        """
        farms = [
            {
                "business_profile":self.samuels_business_profile.id,
                "name": "Samuels Eti Osa Maize Farm",
                "size": "10",
                "commodity": self.commodity_maize.id,
                "farm_address": self.address_eti_osa.id
            },
            {
                "business_profile":self.peters_business_profile.id,
                "name": "Peters Eti Osa Cassava Farm",
                "size": "20",
                "commodity": self.commodity_maize.id,
                "farm_address": self.address_eti_osa_2.id
            }
        ]

        # Permission to Add farm
        add_farm_permission = Permission.objects.get(name="Can add farm")
        self.user.user_permissions.add(add_farm_permission)
        
        self.authenticate()

        for farm in farms:
            response = self.client.post(reverse("farm-list"), format="json", data=farm)
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                msg=f"Failed to create farm: ${response.data} : ${self.user} : for farm: ${farm}",
            )

    # Test if a farm fails to be created successfully
    # using an unauthenticated or unauthorized user
    def test_unsuccessful_farm_creation_using_unaauthenticated_or_unauthorized_user(self):
        """
        Tests that farms fails to be created using
        an unauthenticated or unauthorized user
        """
        farms = [
            {
                "business_profile":self.samuels_business_profile.id,
                "name": "Samuels Eti Osa Maize Farm",
                "size": "10",
                "commodity": self.commodity_maize.id,
                "farm_address": self.address_eti_osa.id
            },
            {
                "business_profile":self.peters_business_profile.id,
                "name": "Peters Eti Osa Cassava Farm",
                "size": "20",
                "commodity": self.commodity_maize.id,
                "farm_address": self.address_eti_osa_2.id
            }
        ]

        for farm in farms:
            response = self.client.post(reverse("farm-list"), format="json", data=farm)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                msg=f"Unauthenticated user is not recieving a 401 status when creating a farm",
            )

        self.authenticate()
        for farm in farms:
            response = self.client.post(reverse("farm-list"), format="json", data=farm)
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
                msg=f"Unauthorized user is not recieving a 403 status when creating a farm",
            )

    # Test if a farm can be updated successfully
    # using put and an authenticated and authorized user
    def test_successful_farm_update_using_put_authenticated_and_authorized_user(self):
        """
        Tests that a farm can be updated successfully 
        using put and an authenticated and authorized user
        """
        updated_farm = {
                "business_profile": self.johns_business_profile.id,
                "name": "Johns Municipal Area Council Cassava Farm",
                "size": "20",
                "commodity": self.commodity_cassava.id,
                "farm_address": self.address_municipal_area_council.id
            }

        # Add the required permission
        # Permission to change farm
        change_farm_permission = Permission.objects.get(name="Can change farm")
        self.user.user_permissions.add(change_farm_permission)


        self.authenticate()
        response = self.client.put(reverse("farm-detail", kwargs={"pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to update farm: ${response.data} : ${self.user} : for farm: ${self.farm}",
        )

        self.assertEqual(response.data["name"], updated_farm["name"])
        self.assertEqual(response.data["commodity"], updated_farm["commodity"])


    # Test if a farm fails to be updated successfully
    # using put and an unauthenticated or unauthorized user
    def test_unsuccessful_farm_update_using_put_unauthenticated_or_unauthorized_user(self):
        """
        Tests if a farm fails to be updated successfully
        using put and an unauthenticated or unauthorized user
        """
        updated_farm = {
                "business_profile": self.johns_business_profile.id,
                "name": "Johns Municipal Area Council Cassava Farm",
                "size": "20",
                "commodity": self.commodity_cassava.id,
                "farm_address": self.address_municipal_area_council.id
            }

        response = self.client.put(reverse("farm-detail", kwargs={"pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when updating a farm using put",
        )

        # Authenticate the user but don't give them permission to change farm
        self.authenticate()
        response = self.client.put(reverse("farm-detail", kwargs={"pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unauthorized user is not recieving a 403 status when updating a farm using put",
        )

    # Test if a farm can be updated successfully
    # using patch and an authenticated and authorized user
    def test_successful_farm_update_using_patch_authenticated_and_authorized_user(self):
        """
        Tests if a farm can be updated successfully
        using patch and an authenticated and authorized user
        """
        updated_farm = {
                "name": "Johns Municipal Area Council Cassava Farm",
                "commodity": self.commodity_cassava.id,
            }

        # Add the required permission
        # Permission to change farm
        change_farm_permission = Permission.objects.get(name="Can change farm")
        self.user.user_permissions.add(change_farm_permission)

        self.authenticate()
        response = self.client.patch(reverse("farm-detail", kwargs={"pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to update farm: ${response.data} : ${self.user} : for farm: ${self.farm}",
        )

        self.assertEqual(response.data["name"], updated_farm["name"])
        self.assertEqual(response.data["commodity"], updated_farm["commodity"])


    # Test if a farm fails to be updted successfully
    # using patch and an unauthenticated or unauthorized user
    def test_unsuccessful_farm_update_using_patch_unauthenticated_and_unauthorized_user(self):
        """
        Test if a farm fails to be updated successfully
        using patch and an unauthenticated or unauthorized user
        """
        updated_farm = {
            "name": "Johns Municipal Area Council Cassava Farm",
            "commodity": self.commodity_cassava.id,
        }

        response = self.client.patch(reverse("farm-detail", kwargs={"pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when updating a farm using patch",
        )

        # Authenticate the user but don't give them permission to change farm
        self.authenticate()
        response = self.client.patch(reverse("farm-detail", kwargs={"pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unauthorized user is not recieving a 403 status when updating a farm using patch",
        )

    # Test if a list of farms can be retrieved successfully
    # using an authenticated user
    def test_successful_farm_list_retrieval_using_authenticated_user(self):
        """
        Test if a list of farms can be retrieved successfully
        using an authenticated user
        """
        self.authenticate()
        response = self.client.get(reverse("farm-list"), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to retrieve farms: ${response.data} : ${self.user}",
        )

        self.assertEqual(
            response.data['count'],
            1,
            msg=f"The number of farms retrieved is incorrect",
        )

    # Test if a list of farms fails to be retrieved 
    # successfully using an unauthenticated user
    # unauthorized users are not checked since any 
    # authenticated user can view a list of farms
    def test_unsuccessful_farm_list_retrieval_using_unauthenticated_user(self):
        """
        Test if a list of farms fails to be retrieved 
        successfully using an unauthenticated user
        """
        response = self.client.get(reverse("farm-list"), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when viewing list of farms",
        )

    # Tests if details of a single farm can be retrieved successfully
    # using an authenticated user
    def test_successful_farm_details_retrieval_using_authenticated_user(self):
        """
        Tests if details of a single farm can be retrieved successfully
        using an authenticated user
        """

        self.authenticate()
        response = self.client.get(reverse("farm-detail", kwargs={"pk": self.farm.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to retrieve farm: ${response.data} : ${self.user} : for farm: ${self.farm}", 
        )

    # Test if details of a single farm fails to be
    # retrieved successfully using an unauthenticated user
    def test_unsuccessful_farm_detail_retrieval_using_unauthenticated_user(self):
        """
        Test if details of a single farm fails to be
        retrieved successfully using an unauthenticated user
        """
        response = self.client.get(reverse("farm-detail", kwargs={"pk": self.farm.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when viewing details of a farm", 
        )

    # Test if a farm can successfully be assigned to new a cluster using
    # an authenticated user
    def test_assign_farm_to_new_cluster_auth_user(self):
        """
        Test if a farm can successfully be assigned to a new cluster
        using an auth user.
        The cluster has to be created based on the details (farm and 
        local goverment area) of the farm
        """
        # Make sure the cluster does not exist initially
        # Try and find the cluster, if it does not exist set cluster to None
        try:
            cluster = Cluster.objects.get(cluster_name="{} {} cluster".format(self.farm.farm_address.local_government_area, self.farm.commodity.commodity_name))
        except Cluster.DoesNotExist:
            cluster = None

            self.assertEqual(
                cluster,
                None,
                msg=f"Cluster exists",
            )

        self.authenticate()
        response = self.client.get(reverse("farm-assign-cluster", kwargs={"pk": self.farm.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to assign farm to cluster ${response}", 
        )
        self.farm.refresh_from_db()
        self.assertEqual(
            self.farm.cluster.cluster_name,
            "{} {} cluster".format(self.farm.farm_address.local_government_area, self.farm.commodity.commodity_name),
            msg=f"Failed to assign farm to cluster",
        )

        # Check if the cluster has been created
        self.assertEqual(
            Cluster.objects.get(cluster_name="{} {} cluster".format(self.farm.farm_address.local_government_area, self.farm.commodity.commodity_name)).cluster_name,
            "{} {} cluster".format(self.farm.farm_address.local_government_area, self.farm.commodity.commodity_name),
            msg=f"Failed to create a new cluster",
        )

    # Test if a farm fails to be successfully be assigned to new a cluster using
    # an unauthenticated user
    def test_unsuccessful_assign_farm_to_new_cluster_unauth_user(self):
        """
        Test if a farm fails to be successfully be assigned to new a cluster using
        an unauthenticated user.
        """
        # Make sure the cluster does not exist initially
        # Try and find the cluster, if it does not exist set cluster to None
        try:
            cluster = Cluster.objects.get(cluster_name="{} {} cluster".format(self.farm.farm_address.local_government_area, self.farm.commodity.commodity_name))
        except Cluster.DoesNotExist:
            cluster = None

            self.assertEqual(
                cluster,
                None,
                msg=f"Cluster exists",
            )

        response = self.client.get(reverse("farm-assign-cluster", kwargs={"pk": self.farm.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when assigning a farm to a cluster", 
        )

    # Test if a farm can successfully be assigned to an existing cluster
    # using an authenticated user
    def test_assign_farm_to_existing_cluster_auth_user(self):
        """
        Test if a farm can successfully be assigned to an existing cluster
        using an authenticated user
        """
        # Create a cluster
        cluster = Cluster.objects.create(
            cluster_name="{} {} cluster".format(self.farm.farm_address.local_government_area, self.farm.commodity.commodity_name),
            local_government_name=self.farm.farm_address.local_government_area,
            commodity=self.farm.commodity
        )
        cluster.save()

        self.authenticate()
        response = self.client.get(reverse("farm-assign-cluster", kwargs={"pk": self.farm.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to assign farm to cluster ${response}", 
        )
        self.farm.refresh_from_db()
        self.assertEqual(
            self.farm.cluster.cluster_name,
            "{} {} cluster".format(self.farm.farm_address.local_government_area, self.farm.commodity.commodity_name),
            msg=f"Failed to assign farm to cluster",
        )

    # Test if a farm fails to be successfully assigned to an existing cluster
    # using an unauthenticated user
    def test_assign_farm_to_existing_cluster_unauth_user(self):
        """
        Test if a farm fails to be successfully assigned to an existing cluster
        using an unauthenticated user
        """
        # Create a cluster
        cluster = Cluster.objects.create(
            cluster_name="{} {} cluster".format(self.farm.farm_address.local_government_area, self.farm.commodity.commodity_name),
            local_government_name=self.farm.farm_address.local_government_area,
            commodity=self.farm.commodity
        )
        cluster.save()

        response = self.client.get(reverse("farm-assign-cluster", kwargs={"pk": self.farm.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when assigning a farm to a cluster", 
        )
