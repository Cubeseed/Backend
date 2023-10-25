from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import UserProfile, UserProfilePhoto, upload_user_profile_image, FarmerProfile
from rest_framework_simplejwt.tokens import RefreshToken
from cubeseed.address.models import Address
from django.test import override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class UserProfileAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Add the neessary permissions
        content_type = ContentType.objects.get_for_model(UserProfile)
        add_permission = Permission.objects.get(content_type=content_type, codename="add_userprofile")
        change_permission = Permission.objects.get(content_type=content_type, codename="change_userprofile")

        # assign the permissions to the user
        self.user.user_permissions.add(add_permission, change_permission)

        # generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"
        
        # Create an Address instance
        self.address = Address.objects.create(
            address="testing 1234",
            locality="Testville",
            administrative_area="Testland",
            country="NG",
            postal_code="12345",
            osm_checked=True,
            osm_latitude=0.0,
            osm_longitude=0.0,
            updated_at="2023-08-27T12:41:06.021393Z",
            created_at="2023-08-27T12:41:06.021348Z"
        )

        # Create a UserProfile associated with the user
        self.user_profile = UserProfile.objects.create(
            full_name = "testuserprofile",
            email = "example@gmail.com",
            phone_number = "1234567890",
            address = self.address,
            about_me = "testing-0987689",
            user = self.user,
            created_at = "2023-08-27T12:41:06.021348Z",
            updated_at = "2023-08-27T12:41:06.021393Z"
        )

    def test_get_userProfile(self):
        # Authenticate as the test user using the JWT token
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)

        # Make the GET request
        response = self.client.get("/api/userprofile/")

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test the POST route
    def test_create_userProfile(self):
        # Authenticate as the test user using the JWT token
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)

        url = reverse("userprofile-list")
        data = {
            "full_name": "testuserprofile-2",
            "email": "example2@gmail.com",
            "phone_number": "1234567890",
            "address": self.address.id,
            "about_me": "testing-0987689",
            "user": self.user.id
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth_header, format="json")

        #verify that the user profile is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 2)
        user_profile = UserProfile.objects.get(full_name="testuserprofile-2")
        self.assertEqual(user_profile.full_name, "testuserprofile-2")
        self.assertEqual(user_profile.phone_number, "1234567890")
        self.assertEqual(user_profile.address, self.address)
        self.assertEqual(user_profile.about_me, "testing-0987689")
        self.assertEqual(user_profile.user, self.user)


class FarmerProfileAPITestCase(APITestCase):
    """For testing the FarmProfile API"""
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Add the neessary permissions
        content_type = ContentType.objects.get_for_model(FarmerProfile)
        add_permission = Permission.objects.get(content_type=content_type, codename="add_farmerprofile")
        change_permission = Permission.objects.get(content_type=content_type, codename="change_farmerprofile")

        # assign the permissions to the user
        self.user.user_permissions.add(add_permission, change_permission)

        # Generate the token and add it to the auth header
        refresh = RefreshToken.for_user(self.user)
        self.token_value = str(refresh.access_token)
        self.auth_header = f"Bearer {self.token_value}"
        # Create an Address instance
        self.address = Address.objects.create(
            address="testing 1234",
            locality="Testville",
            administrative_area="Testland",
            country="NG",
            postal_code="12345",
            osm_checked=True,
            osm_latitude=0.0,
            osm_longitude=0.0,
            updated_at="2023-08-27T12:41:06.021393Z",
            created_at="2023-08-27T12:41:06.021348Z"
        )

        # Create a UserProfile instance associated with the user
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            full_name="Test User",
            phone_number="1234567890",
            address=self.address
        )

    # Test the POST route
    def test_create_farmer_profile(self):
        url = reverse("farmerprofile-list")
        data = {
            "review_status": "P",
            "reviewed_by": None,
            "user_profile": self.user_profile.id
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=self.auth_header, format="json")

        #verify that the farmer profile is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FarmerProfile.objects.count(), 1)
        farmer_profile = FarmerProfile.objects.get()
        self.assertEqual(farmer_profile.review_status, "P")
        self.assertIsNone(farmer_profile.reviewed_by)
        self.assertEqual(farmer_profile.user_profile, self.user_profile)

    # Test the GET route
    def test_get_farmer_profile(self):
        #create a farmer profile
        farmer_profile = FarmerProfile.objects.create(
            review_status = "P",
            reviewed_by = None,
            user_profile = self.user_profile
        )

        # define the url for retrieving the farmer profile by it'S id
        url = reverse("farmerprofile-detail", args=[farmer_profile.id])

        # make the GET request
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth_header)

        # verification
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verfify that the returned data matches the farmer profile created
        self.assertEqual(response.data["review_status"], "P")
        self.assertEqual(response.data["user_profile"], self.user_profile.id)

    # Test the PUT route
    def test_update_farmer_profile(self):
        #create a farmer profile
        farmer_profile = FarmerProfile.objects.create(
            review_status = "P",
            reviewed_by = None,
            user_profile = self.user_profile
        )

        # define the url for updating the farmer profile by it'S id
        url = reverse("farmerprofile-detail", args=[farmer_profile.id])

        # make the PUT request
        data = {
            "review_status": "A",
            "reviewed_by": None,
            "user_profile": self.user_profile.id
        }
        response = self.client.put(url, data, HTTP_AUTHORIZATION=self.auth_header, format="json")

        # verification
        self.assertEqual(response.status_code, status.HTTP_200_OK)

         # Reload the FarmerProfile from the database to check for updates
        farmer_profile.refresh_from_db()

        # verfify that the returned data mathches the farmer profile created
        self.assertEqual(response.data["review_status"], "A")
        self.assertEqual(response.data["user_profile"], self.user_profile.id)

    # Test the PATCH route
    def test_partial_update_farmer_profile(self):
        #create a farmer profile
        farmer_profile = FarmerProfile.objects.create(
            review_status = "P",
            reviewed_by = None,
            user_profile = self.user_profile
        )

        # define the url for updating the farmer profile by it'S id
        url = reverse("farmerprofile-detail", args=[farmer_profile.id])

        # make the PATCH request
        data = {
            "review_status": "A"
        }
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=self.auth_header, format="json")

        # verification
        self.assertEqual(response.status_code, status.HTTP_200_OK)

         # Reload the FarmerProfile from the database to check for updates
        farmer_profile.refresh_from_db()

        # verfify that the returned data mathches the farmer profile created
        self.assertEqual(response.data["review_status"], "A")
        self.assertEqual(response.data["user_profile"], self.user_profile.id)
