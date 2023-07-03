import logging
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cubeseed.userauth.serializers import UserSerializer, GroupSerializer, RegisterUserSerializer


logger = logging.getLogger(__name__)

class UserAuthTest(APITestCase):
    def test_register_user_auth(self):
        logger.debug('Adding a new user into database')
        data = {
            "username": "goEmtEPOI+riADh0EFF8D0mS5h_",
            "email": "user@example.com",
            "groups": [
                "string"
            ],
            "password": "stringst"
        }
