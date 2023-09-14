from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from cubeseed.commodity.models import Commodity
from rest_framework import status
from .models import Cluster

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
                msg=f"Failed to create cluster: ${response.data} : ${self.user} : for cluster: ${cluster}",
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
            msg=f"Failed to update cluster: ${response.data} : ${self.user} : for cluster: ${updated_cluster}",
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
            msg=f"Failed to update cluster: ${response.data} : ${self.user} : for cluster: ${updated_cluster}",
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
            msg=f"Failed to update cluster: ${response.data} : ${self.user} : for cluster: ${updated_cluster}",
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
            msg=f"Failed to update cluster: ${response.data} : ${self.user} : for cluster: ${updated_cluster}",
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
            msg=f"Failed to delete cluster: ${response.data} : ${self.user} : for cluster: ${self.cluster_eti_osa_maize}",
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
            msg=f"Failed to retrieve clusters: ${response.data} : ${self.user}",
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
            msg=f"Failed to retrieve cluster: ${response.data} : ${self.user} : for cluster: ${self.cluster_eti_osa_maize}", 
        )


    

