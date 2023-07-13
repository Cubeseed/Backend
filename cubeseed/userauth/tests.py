from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthAPITest(APITestCase):
    """
    contains the API test cases for User Auth
    """
    def setUp(self):
        self.url = reverse('user-list')
        # self.group = Group.objects.create(name='market')

    def authenticate(self):
         User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
         
         response = self.client.post(reverse('token_obtain_pair'),{
             'username':'testuser',
            'password':'testpassword'
         })
         token = response.data['access']
         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_user_list(self):
        """
        Test to get all the users in the db
        """
        self.authenticate()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(User.objects.count(), 2)

    def test_register_user(self):
        """
        Adds a test user into the database
        """
        data = {
            "username": "user2",
            "email": "user2@example.com",
            "groups": ['http://testserver/api/userauth/groups/3/'],
            "password": "stringst",
            'is_active': True
        }

        self.authenticate()
        response = self.client.post(reverse("register-list"), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["username"], data["username"])

    def test_register_user_with_invalid_data(self):
        """
        Adds a test with invalid data
        """
        #register a new user with invalid data
        invalid_data = {
            'username': 'testinvaliduser',
            'email': 'invalidemail',  # Invalid email format
            'password': 'testpassword',
            'groups': ["farmer"]
        }

        response = self.client.post(reverse("register-list"), invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify that the user is not created in the database
        self.assertEqual(get_user_model().objects.count(), 1)

    #     # Verify that the response contains an error for the 'email' field
    #     # self.assertIn('email', response.data)

    def test_list_groups(self):
        self.authenticate()

        response = self.client.get(reverse('group-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 7)
