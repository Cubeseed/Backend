from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import BusinessProfile
from rest_framework_simplejwt.tokens import RefreshToken

class BusinessProfileAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"


        # Create a BusinessProfile associated with the user
        self.business_profile = BusinessProfile.objects.create(
            user=self.user,
            business_name="testbusinessprofile",
            email="testbusiness1@example.com",
            telephone="testing-1234",
            billing_address="testing-1111",
            shipping_address="testing-0987689",
            logo="null",
            document_type="test-file",
            created_at="2023-08-27T12:41:06.021348Z",
            updated_at="2023-08-27T12:41:06.021393Z"
        )

    # Testing the GET all the businessprofiles route
    def test_list_business_profile(self):
        url = reverse("businessprofile-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing the POST(create) route
    def test_create_business_profiles(self):
        url = reverse("businessprofile-list")
        data = {
            "business_name": "New Business",  # Corrected field name
            "email": "newbusiness@example.com",
            "telephone": "1234567890",
            "billing_address": "123 Main St",
            "shipping_address": "456 Elm St",
            "document_type": "TIN"
        }
        response = self.client.post(url, data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testing GET business profile by id route
    def test_get_business_profiles_by_id(self):
        url = reverse("businessprofile-detail", args=[self.business_profile.id])
        response = self.client.get(url, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testing the PUT(update) businessprofile by id route
    def test_put_business_profile_by_id(self):
        # Get the URL for the specific business profile by its ID
        url = reverse("businessprofile-detail", args=[self.business_profile.id])

        # Data for updating the business profile
        updated_data = {
            "business_name": "Updated Business",
            "telephone": "9876543210",
            "email": "null",
            "billing_address": "00000",
            "shipping_address": "004400",
            "document_type": "PITIN"
        }

        # Make a PUT request to update the business profile
        response = self.client.put(url, updated_data, format="json", HTTP_AUTHORIZATION=self.auth_header)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the business profile from the test database and check if it's updated
        self.business_profile.refresh_from_db()
        self.assertEqual(self.business_profile.business_name, updated_data["business_name"])
        self.assertEqual(self.business_profile.telephone, updated_data["telephone"])
        self.assertEqual(self.business_profile.email, updated_data["email"])
        self.assertEqual(self.business_profile.billing_address, updated_data["billing_address"])
        self.assertEqual(self.business_profile.shipping_address, updated_data["shipping_address"])
        self.assertEqual(self.business_profile.document_type, updated_data["document_type"])


    # Testing PATCH(partial updating) the specific business profile by it's id
    def test_patch_business_profile_by_id(self):
        url = reverse("businessprofile-detail", args=[self.business_profile.id])
        partial_update_data = {
            "business_name": "Updated Business-2"
        }

        #send the patch request
        response = self.client.patch(url, partial_update_data, format="json", HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #refresh test db and check if it's updated
        self.business_profile.refresh_from_db()
        self.assertEqual(self.business_profile.business_name, partial_update_data["business_name"])
