from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthAPITest(APITestCase):
    """
    contains the API test cases for User Auth
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})

    def authenticate(self):
         permission_change = Permission.objects.get(codename='change_user')
         permission_delete = Permission.objects.get(codename='delete_user')
         self.user.user_permissions.add(permission_change, permission_delete)

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
        response = self.client.get(reverse('user-list'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # count all the users including admin
        self.assertEqual(User.objects.count(), 2)

    def test_register_user(self):
        """
        Adds a test user into the database
        """
        data = {
            "username": "user2",
            "email": "user2@example.com",
            "groups": [2],
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
        self.assertEqual(User.objects.count(), 2)


    def test_list_groups(self):
        self.authenticate()

        response = self.client.get(reverse('group-list'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # returns the number of groups original created in the migration folder
        self.assertEqual(response.data['count'], 7)

    def test_get_user(self):
        self.authenticate()

        
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_user(self):
        self.authenticate()

        updated_data = {
            "username": "testuser2"
        }
        response = self.client.put(self.url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], updated_data['username'])

    def test_delete_user(self):
        self.authenticate()

        response = self.client.delete(self.url,  format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)