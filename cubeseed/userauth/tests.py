from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase ,force_authenticate
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
#from cubeseed.userauth.serializers import UserSerializer, GroupSerializer, RegisterUserSerializer

class UserAuthAPITest(APITestCase):
    """
    contains the API test cases for User Auth
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',  password='testpassword')
        self.group = Group.objects.create(name='Test Group')

    def test_register_user(self):
        """
        Adds a test user into the database
        """
        data = {
            "username": "goEmtEPOI+riADh0EFF8D0mS5h_",
            "email": "user@example.com",
            "groups": ["market"],
            "password": "stringst"
        }
        url = reverse('userauth/register')
        request = self.client.post(url, data, format='json')
        force_authenticate(request, user=self.user)
        response = request + 'HTTP_AUTHORIZATION' +':'+ 'Token ' + self.user.auth_token.key

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the user is created in the database
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_register_user_with_invalid_data(self):
        """
        Adds a test with invalid data
        """
        invalid_data = {
            'username': 'testinvaliduser',
            'email': 'invalidemail',  # Invalid email format
            'password': 'testpassword',
            'groups': ["farmer"],
            'is_active': False,
        }
        url = reverse('userauth/register')
        request = self.client.post(url, invalid_data, format='json')
        force_authenticate(request, user=self.user)
        response = request + 'HTTP_AUTHORIZATION' +':'+ 'Token ' + self.user.auth_token.key

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify that the user is not created in the database
        self.assertEqual(get_user_model().objects.count(), 1)

        # Verify that the response contains an error for the 'email' field
        self.assertIn('email', response.results)

    def test_get_user_list(self):
        """
        Test to get all the users in the db
        """
        self.test_register_user()

        url = reverse('userauth/users')
        request = self.client.get(url, format='json')
        force_authenticate(request, user=self.user)
        response = request + 'HTTP_AUTHORIZATION' +':'+ 'Token ' + self.user.auth_token.key

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.results['username'], self.user.username)
