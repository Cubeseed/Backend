from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from .models import Commodity

# Create your tests here.
User = get_user_model()
class CommodityAPITest(APITestCase):
    def setUp(self) -> None:
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user.is_active = True
        self.user.groups.add(Group.objects.get(name="farmer"))

        self.user.save()
        self.url = reverse("user-detail", kwargs={"pk": self.user.pk})

        # Create a commodity
        self.commodity_corn = Commodity.objects.create(commodity_name="Corn")
        
    def authenticate(self):
        token_response = self.client.post(
            reverse("token_obtain_pair"), {"username": "testuser", "password": "testpassword"}
        )
        access_token = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Test if a commodity can be created successfully
    # using an authenticated user
    def test_successful_commodity_creation_using_auth_user(self):
        """
        Tests that a commodity can be created
        successfully using an authenticated user
        """
        commodities = [
            {
                "commodity_name": "Maize",
            },
            {
                "commodity_name": "Cassava"
            }
        ]

        self.authenticate()
        for commodity in commodities:
            response = self.client.post(reverse("commodity-list"), format="json", data=commodity)
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                msg=f"Failed to create commodity: ${response.data} : ${self.user} : for commodity: ${commodity}",
            )

        
    # Test if a commodity fails to be created successfully
    # using an unauthenticated user
    def test_unsuccessful_commodity_creation_using_unauth_user(self):
        """
        Tests that a commodity fails to be created
        successfully using an unauthenticated user
        """
        commodities = [
            {
                "commodity_name": "Maize",
            },
            {
                "commodity_name": "Cassava"
            }
        ]

        for commodity in commodities:
            response = self.client.post(reverse("commodity-list"), format="json", data=commodity)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                msg=f"Unauthenticated user is not recieving a 401 status when creating a commodity",
            )
    
    # Tests if a commodity can be updated successfully
    # using put and an authenticated user
    def test_successful_commodity_update_using_put_and_auth_user(self):
        """
        Tests that a commodity can be updated
        successfully using put and an authenticated user
        """
        updated_commodity = {
                "commodity_name": "Maize",
            }
        
        self.authenticate()
        response = self.client.put(reverse("commodity-detail", kwargs={"pk": self.commodity_corn.id}), format="json", data=updated_commodity)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to update commodity: ${response.data} : ${self.user} : for commodity: ${updated_commodity}",
        )

        self.assertEqual(response.data["commodity_name"], updated_commodity["commodity_name"])

    # Tests if a commodity fails to be updated successfully
    # using put and an unauthenticated user
    def test_unsuccessful_commodity_update_using_put_and_unauth_user(self):
        """
        Tests if a commodity fails to be updated successfully
        using put and an unauthenticated user
        """
        updated_commodity = {
                "commodity_name": "Maize",
            }
        
        response = self.client.put(reverse("commodity-detail", kwargs={"pk": self.commodity_corn.id}), format="json", data=updated_commodity)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when updating a commodity using put",
        )

    # Tests if a commodity can be updated successfully
    # using patch and an authenticated user
    def test_successful_commodity_update_using_patch_and_auth_user(self):
        """
        Tests that a commodity can be updated
        successfully using patch and an authenticated user
        """
        updated_commodity = {
                "commodity_name": "Maize",
            }
        
        self.authenticate()
        response = self.client.patch(reverse("commodity-detail", kwargs={"pk": self.commodity_corn.id}), format="json", data=updated_commodity)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to update commodity: ${response.data} : ${self.user} : for commodity: ${updated_commodity}",
        )

        self.assertEqual(response.data["commodity_name"], updated_commodity["commodity_name"])

    # Tests if a commodity fails to be updated successfully
    # using patch and an unauthenticated user
    def test_unsuccessful_commodity_update_using_patch_and_unauth_user(self):
        """
        Tests if a commodity fails to be updated successfully
        using patch and an unauthenticated user
        """
        updated_commodity = {
                "commodity_name": "Maize",
            }
        
        response = self.client.patch(reverse("commodity-detail", kwargs={"pk": self.commodity_corn.id}), format="json", data=updated_commodity)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when updating a commodity using patch",
        )


    # Tests if a commodity can be deleted successfully
    # using an authenticated user
    def test_successful_commodity_delete_using_auth_user(self):
        """
        Tests that a commodity can be deleted
        successfully using an authenticated user
        """
        self.authenticate()
        response = self.client.delete(reverse("commodity-detail", kwargs={"pk": self.commodity_corn.id}), format="json")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            msg=f"Failed to delete commodity: ${response.data} : ${self.user} : for commodity: ${self.commodity_corn}",
        )

    # Tests unsuccessful commodity delete using an 
    # unauthenticated user
    def test_unsuccessful_commodity_delete_using_unauth_user(self):
        """
        Tests unsuccessful commodity delete using an unauthenticated user
        """
        response = self.client.delete(reverse("commodity-detail", kwargs={"pk": self.commodity_corn.id}), format="json")
        
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when deleting a commodity",
        )
    
    # Tests if a list of commodities can be retrieved successfully
    # using an authenticated user
    def test_successful_commodity_list_retrieval_using_auth_user(self):
        """
        Tests that a list of commodities can be retrieved
        successfully using an authenticated user
        """
        self.authenticate()
        response = self.client.get(reverse("commodity-list"), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to retrieve commodities: ${response.data} : ${self.user}",
        )

        self.assertEqual(
            response.data['count'],
            1,
            msg=f"The number of commodities retrieved is incorrect",
        )

    # Tests if a list of commodities fails to be retrieved successfully
    # using an unauthenticated user
    def test_unsuccessful_commodity_list_retrieval_using_unauth_user(self):
        """
        Tests if a list of commodities fails to be retrieved successfully
        using an unauthenticated user
        """
        response = self.client.get(reverse("commodity-list"), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when viewing the list of commodities",
        )
        
    # Tests if details of a single commodity can be retrieved successfully
    # using an authenticated user
    def test_successful_commodity_details_retrieval_using_auth_user(self):
        """
        Tests that details of a single commodity can be retrieved
        successfully using an authenticated user
        """
        self.authenticate()
        response = self.client.get(reverse("commodity-detail", kwargs={"pk": self.commodity_corn.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=f"Failed to retrieve commodity: ${response.data} : ${self.user} : for commodity: ${self.commodity_corn}", 
        )

    # Tests if details of a single commodity fails to be retrieved successfully
    # using an unauthenticated user
    def test_unsuccessful_commodity_details_retrieval_using_unauth_user(self):
        """
        Tests if details of a single commodity fails to be retrieved successfully
        using an unauthenticated user
        """

        response = self.client.get(reverse("commodity-detail", kwargs={"pk": self.commodity_corn.id}), format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=f"Unauthenticated user is not recieving a 401 status when viewing details of a commodity", 
        )

    