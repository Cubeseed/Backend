from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth.models import Permission
from cubeseed.commodity.models import Commodity
from rest_framework import status
from .models import Cluster
from cubeseed.commodity.models import Commodity
from cubeseed.address.models import Address
from cubeseed.businessprofile.models import BusinessProfile
from cubeseed.farm.models import Farm


# Create your tests here.
User = get_user_model()
class ClusterAPITest(APITestCase):
    def setUp(self) -> None:
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

        # Create a Cluster
        self.cluster_eti_osa_maize = Cluster.objects.create(
                cluster_name="Eti Osa Maize Cluster",
                local_government_name="Eti Osa",
                commodity=self.commodity_maize
        )
        self.cluster_eti_osa_maize.save()
        
    def authenticate(self):
        token_response = self.client.post(
            reverse("token_obtain_pair"), {"username": "testuser", "password": "testpassword"}
        )
        access_token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Test if a cluster can be created successfully
    # using an authenticated user
    def test_successful_cluster_creation_using_auth_user(self):
        """
        Tests that a cluster can be created
        successfully using an authenticated user
        """
        clusters = [
            {
                "cluster_name": "Eti Osa Maize Cluster",
                "local_government_name": "Eti Osa",
                "commodity": 1
            },
            {
                "cluster_name": "Eti Osa Cassava Cluster",
                "local_government_name": "Eti Osa",
                "commodity": 2
            }
        ]

        self.authenticate()
        for cluster in clusters:
            response = self.client.post(reverse("cluster-list"), format="json", data=cluster)
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                msg=f"Failed to create cluster: ${response.data} : ${self.user} : for cluster: ${cluster}",
            )

        

    # Test if a cluster fails to be created successfully
    # using an unauthenticated user
    def test_unsuccessful_cluster_creation_using_unauth_user(self):
        """
        Tests that a cluster fails to be created
        successfully using an unauthenticated user
        """
        clusters = [
            {
                "cluster_name": "Eti Osa Maize Cluster",
                "local_government_name": "Eti Osa",
                "commodity": 1
            },
            {
                "cluster_name": "Eti Osa Cassava Cluster",
                "local_government_name": "Eti Osa",
                "commodity": 2
            }
        ]

        for cluster in clusters:
            response = self.client.post(reverse("cluster-list"), format="json", data=cluster)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                msg=f"Unauthenticated user is not recieving a 401 status when creating a cluster",
            )
        

    # Tests if a cluster can be updated successfully
    # using put and an authenticated user
    def test_successful_cluster_update_using_put_and_auth_user(self):
        """
        Tests that a cluster can be updated
        successfully using put and an authenticated user
        """
        updated_cluster = {
                "cluster_name": "Aba North Cassava Cluster",
                "local_government_name": "Aba North",
                "commodity": 2
            }
        
        self.authenticate()
        response = self.client.put(reverse("cluster-detail", kwargs={"pk": self.cluster_eti_osa_maize.id}), format="json", data=updated_cluster)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to update cluster: ${response.data} : ${self.user} : for cluster: ${self.cluster_eti_osa_maize}",
        )

        self.assertEqual(response.data["cluster_name"], updated_cluster["cluster_name"])
        self.assertEqual(response.data["local_government_name"], updated_cluster["local_government_name"])
        self.assertEqual(response.data["commodity"], updated_cluster["commodity"])


    # Tests if a cluster fails to be updated successfully
    # using an unauthenticated user
    def test_unsuccessful_cluster_update_using_unauth_user(self):
        """
        Tests that a cluster fails to be updated successfully
        using an unauthenticated user
        """
        updated_cluster = {
                "cluster_name": "Aba North Cassava Cluster",
                "local_government_name": "Aba North",
                "commodity": 2
            }
        
        response = self.client.put(reverse("cluster-detail", kwargs={"pk": self.cluster_eti_osa_maize.id}), format="json", data=updated_cluster)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when updating a cluster using put",
        )
      
    # Tests if a cluster can be updated successfully
    # using patch and an authenticated user
    def test_successful_cluster_update_using_patch_and_auth_user(self):
        """
        Tests that a cluster can be updated
        successfully using patch and an authenticated user
        """
        updated_cluster = {
                "cluster_name": "Aba North Maize Cluster",
                "commodity": 1
            }
        
        self.authenticate()
        response = self.client.patch(reverse("cluster-detail", kwargs={"pk": self.cluster_eti_osa_maize.id}), format="json", data=updated_cluster)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to update cluster: ${response.data} : ${self.user} : for cluster: ${self.cluster_eti_osa_maize}",
        )

        self.assertEqual(response.data["cluster_name"], updated_cluster["cluster_name"])
        self.assertEqual(response.data["commodity"], updated_cluster["commodity"])


    # Tests if a cluster fails to be updated successfully
    # using patch and an unauthenticated user
    def test_unsuccessful_cluster_update_using_patch_and_unauth_user(self):
        """
        Tests that a cluster fails to be updated successfully
        using patch and an unauthenticated user
        """
        updated_cluster = {
                "cluster_name": "Aba North Maize Cluster",
                "commodity": 1
            }
        
        response = self.client.patch(reverse("cluster-detail", kwargs={"pk": self.cluster_eti_osa_maize.id}), format="json", data=updated_cluster)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when updating a cluster using patch",
        )


    # Tests if a cluster can be deleted successfully
    # using an authenticated user
    def test_successful_cluster_delete_using_auth_user(self):
        """
        Tests that a cluster can be deleted
        successfully using an authenticated user
        """
        self.authenticate()
        response = self.client.delete(reverse("cluster-detail", kwargs={"pk": self.cluster_eti_osa_maize.id}), format="json")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg=f"Failed to delete cluster: ${response.data} : ${self.user} : for cluster: ${self.cluster_eti_osa_maize}",
        )

    # Tests if a cluster fails to be deleted successfully
    # using an unauthenticated user
    def test_unsuccessful_cluster_delete_using_unauth_user(self):
        """
        Tests that a cluster fails to be deleted successfully
        using an unauthenticated user
        """
        response = self.client.delete(reverse("cluster-detail", kwargs={"pk": self.cluster_eti_osa_maize.id}), format="json")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when deleting a cluster",
        )

    # Tests if a list of cluster can be retrieved successfully
    # using an authenticated user
    def test_successful_cluster_list_retrieval_using_auth_user(self):
        """
        Tests that a list of cluster can be retrieved
        successfully using an authenticated user
        """
        self.authenticate()
        response = self.client.get(reverse("cluster-list"), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to retrieve clusters: ${response.data} : ${self.user}",
        )
    
    # Tests if a list of cluster fails to be retrieved successfully
    # using an unauthenticated user
    def test_unsuccessful_cluster_list_retrieval_using_unauth_user(self):
        """
        Tests that a list of cluster fails to be retrieved successfully
        using an unauthenticated user
        """
        response = self.client.get(reverse("cluster-list"), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when viewing the list of clusters",
        )

    # Tests if details of a single cluster can be retrieved successfully
    # using an authenticated user
    def test_successful_cluster_details_retrieval_using_auth_user(self):
        """
        Tests that details of a single cluster can be retrieved
        successfully using an authenticated user
        """
        self.authenticate()
        response = self.client.get(reverse("cluster-detail", kwargs={"pk": self.cluster_eti_osa_maize.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to retrieve cluster: ${response.data} : ${self.user} : for cluster: ${self.cluster_eti_osa_maize}", 
        )

    # Tests if details of a single cluster fails to be retrieved successfully
    # using an unauthenticated user
    def test_unsuccessful_cluster_details_retrieval_using_unauth_user(self):
        """
        Tests that details of a single cluster fails to be retrieved successfully
        using an unauthenticated user
        """
        response = self.client.get(reverse("cluster-detail", kwargs={"pk": self.cluster_eti_osa_maize.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when viewing details of a cluster", 
        )




class FarmsInClusterAPITest(APITestCase):
    """
    Tests for nested routes (farms in a cluster)
    """
    
    def setUp(self) -> None:
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

        # Create a Cluster (Maize Cluster in Eti Osa)
        self.cluster_eti_osa_maize = Cluster.objects.create(
                cluster_name="Eti Osa Maize Cluster",
                local_government_name="Eti Osa",
                commodity=self.commodity_maize
        )
        self.cluster_eti_osa_maize.save()

        # # Create a Cluster (Cassava Cluster in Eti Osa)
        # self.cluster_eti_osa_cassava = Cluster.objects.create(
        #         cluster_name="Eti Osa Cassava Cluster",
        #         local_government_name="Eti Osa",
        #         commodity=self.commodity_cassava
        # )
        # self.cluster_eti_osa_cassava.save()
        
    def authenticate(self):
        token_response = self.client.post(
            reverse("token_obtain_pair"), {"username": "testuser", "password": "testpassword"}
        )
        access_token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Test if a farm can be created successfully
    # using an authenticated and authorized user
    def test_successful_farm_in_cluster_creation_using_authenticated_and_authorized_user(self):
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
                "name": "Peters Eti Osa Maize Farm",
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
            response = self.client.post(reverse("cluster-farm-list", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id}), format="json", data=farm)
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                msg=f"Failed to create farm in cluster: ${response.data} : ${self.user} : for farm: ${farm}",
            )

        # Check if samuels farm was assigned to the correct cluster
        self.assertEqual(
            Farm.objects.get(business_profile=self.samuels_business_profile.id).cluster.id,
            self.cluster_eti_osa_maize.id,
            msg=f"Failed to create farm in the correct cluster",
        )

        # Check if peters farm was assinged to the correct cluster
        self.assertEqual(
            Farm.objects.get(business_profile=self.peters_business_profile.id).cluster.id,
            self.cluster_eti_osa_maize.id,
            msg=f"Failed to create farm in the correct cluster",
        )

    
    # Test if a farm in cluster fails to be created successfully
    # using an unauthenticated or unauthorized user
    def test_unsuccessful_farm_in_cluster_creation_using_unaauthenticated_or_unauthorized_user(self):
        """
        Tests that farm in cluster fails to be created using
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
                "name": "Peters Eti Osa Maize Farm",
                "size": "20",
                "commodity": self.commodity_maize.id,
                "farm_address": self.address_eti_osa_2.id
            }
        ]

        for farm in farms:
            response = self.client.post(reverse("cluster-farm-list", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id}), format="json", data=farm)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                msg=f"Unauthenticated user is not recieving a 401 status when creating a farm in a cluster",
            )

        self.authenticate()
        for farm in farms:
            response = self.client.post(reverse("cluster-farm-list", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id}), format="json", data=farm)
            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
                msg=f"Unauthorized user is not recieving a 403 status when creating a farm in a cluster",
            )

    # Test if a farm in cluster can be updated successfully
    # using put and an authenticated and authorized user
    def test_successful_farm_in_cluster_update_using_put_authenticated_and_authorized_user(self):
        """
        Tests that a farm in cluster can be updated
        successfully using put and an authenticated
        and authorized user
        """
        # Assign farm to cluster
        self.farm.cluster = self.cluster_eti_osa_maize
        self.farm.save()

        updated_farm = {
                "business_profile": self.johns_business_profile.id,
                "name": "Johns Municipal Area Council Cassava Farm",
                "size": "50.00",
                "commodity": self.commodity_maize.id,
                "farm_address": self.address_eti_osa.id
            }

        # Add the required permission
        # Permission to change farm
        change_farm_permission = Permission.objects.get(name="Can change farm")
        self.user.user_permissions.add(change_farm_permission)


        self.authenticate()
        response = self.client.put(reverse("cluster-farm-detail", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id, "pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to update farm in cluster: ${response.data} : ${self.user} : for farm: ${self.farm}",
        )

        self.assertEqual(response.data["name"], updated_farm["name"])
        self.assertEqual(response.data["size"], updated_farm["size"])


    # Test if a farm in cluster fails to be updated successfully
    # using put and an unauthenticated or unauthorized user
    def test_unsuccessful_farm_in_cluster_update_using_put_unaauthenticated_or_unauthorized_user(self):
        """
        Tests that farm in cluster fails to be updated using
        put and an unauthenticated or unauthorized user
        """
        # Assign farm to cluster
        self.farm.cluster = self.cluster_eti_osa_maize
        self.farm.save()

        updated_farm = {
                "business_profile": self.johns_business_profile.id,
                "name": "Johns Municipal Area Council Cassava Farm",
                "size": "50",
                "commodity": self.commodity_maize.id,
                "farm_address": self.address_eti_osa.id
            }

        response = self.client.put(reverse("cluster-farm-detail", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id, "pk": self.farm.id}), format="json", data=updated_farm)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when updating a farm in a cluster using put",
        )
        self.authenticate()
        response = self.client.put(reverse("cluster-farm-detail", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id, "pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unauthorized user is not recieving a 403 status when updating a farm in a cluster using put",
        )

    # Test if a farm in cluster can be updated successfully
    # using patch and an authenticated and authorized user
    def test_successful_farm_in_cluster_update_using_patch_authenticated_and_authorized_user(self):
        """
        Tests that a farm in cluster can be updated
        successfully using patch and an authenticated
        and authorized user
        """
        # Assign farm to cluster
        self.farm.cluster = self.cluster_eti_osa_maize
        self.farm.save()

        updated_farm = {
                "name": "Johns Municipal Area Council Cassava Farm",
                "size": "50.00",
            }

        # Add the required permission
        # Permission to change farm
        change_farm_permission = Permission.objects.get(name="Can change farm")
        self.user.user_permissions.add(change_farm_permission)


        self.authenticate()
        response = self.client.patch(reverse("cluster-farm-detail", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id, "pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to update farm: ${response.data} : ${self.user} : for farm: ${self.farm}",
        )

        self.assertEqual(response.data["name"], updated_farm["name"])
        self.assertEqual(response.data["size"], updated_farm["size"])


    # Test if a farm in cluster fails to be updated successfully
    # using patch and an unauthenticated or unauthorized user
    def test_unsuccessful_farm_in_cluster_update_using_patch_unaauthenticated_or_unauthorized_user(self):
        """
        Tests that farm in cluster fails to be updated using
        patch and an unauthenticated or unauthorized user
        """
        # Assign farm to cluster
        self.farm.cluster = self.cluster_eti_osa_maize
        self.farm.save()

        updated_farm = {
                "business_profile": self.johns_business_profile.id,
                "name": "Johns Municipal Area Council Cassava Farm",
                "size": "50",
                "commodity": self.commodity_maize.id,
                "farm_address": self.address_eti_osa.id
            }

        response = self.client.patch(reverse("cluster-farm-detail", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id, "pk": self.farm.id}), format="json", data=updated_farm)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when updating a farm in a cluster using patch",
        )
        self.authenticate()
        response = self.client.patch(reverse("cluster-farm-detail", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id, "pk": self.farm.id}), format="json", data=updated_farm)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg=f"Unauthorized user is not recieving a 403 status when updating a farm in a cluster using patch",
        )

    # Test if a list of farms in cluster can be retrieved successfully
    # using an authenticated user
    def test_successful_farm_in_cluster_list_retrieval_using_authenticated_user(self):
        """
        Test if a list of farms in cluster can be retrieved successfully
        using an authenticated user
        """
        # Assign farm to cluster
        self.farm.cluster = self.cluster_eti_osa_maize
        self.farm.save()

        self.authenticate()
        response = self.client.get(reverse("cluster-farm-list", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to retrieve farms: ${response.data} : ${self.user}",
        )

        self.assertEqual(
            response.data['count'],
            1,
            msg=f"The number of farms in cluster retrieved is incorrect",
        )

    # Test if a list of farms in cluster cannot be retrieved successfully
    # using an unauthenticated user
    def test_unsuccessful_farm_in_cluster_list_retrieval_using_unauthenticated_user(self):
        """
        Test if a list of farms in cluster fails to be retrieved successfully
        using an unauthenticated user
        """
        # Assign farm to cluster
        self.farm.cluster = self.cluster_eti_osa_maize
        self.farm.save()

        
        response = self.client.get(reverse("cluster-farm-list", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when viewing the list of farms in a cluster",
        )

    # Tests if details of a single farm within a cluster can
    # be retrieved successfully using an authenticated user
    def test_successful_farm_in_cluster_details_retrieval_using_authenticated_user(self):
        """
        Tests if details of a single farm within a cluster can
        be retrieved successfully using an authenticated user
        """
        # Assign farm to cluster
        self.farm.cluster = self.cluster_eti_osa_maize
        self.farm.save()

        # Add the required permission
        # Permission to change farm
        change_farm_permission = Permission.objects.get(name="Can change farm")
        self.user.user_permissions.add(change_farm_permission)


        self.authenticate()
        response = self.client.get(reverse("cluster-farm-detail", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id, "pk": self.farm.id}), format="json")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to retrieve details of farm in a cluster"
        )

    # Tests if details of a single farm within a cluster fails
    # to be retrieved using an unauthenticated user
    def test_unsuccessful_farm_in_cluster_details_retrieval_using_unauthenticated_user(self):
        """
        Tests if details of a single farm within a cluster fails
        to be retrieved using an unauthenticated user
        """
        # Assign farm to cluster
        self.farm.cluster = self.cluster_eti_osa_maize
        self.farm.save()

        # Add the required permission
        # Permission to change farm
        change_farm_permission = Permission.objects.get(name="Can change farm")
        self.user.user_permissions.add(change_farm_permission)

        response = self.client.get(reverse("cluster-farm-detail", kwargs={"cluster_pk": self.cluster_eti_osa_maize.id, "pk": self.farm.id}), format="json")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when viewing details of a farm withing a cluster"
        )