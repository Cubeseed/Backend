from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from userprofile.models import UserProfile, UserProfilePhoto
from userprofile.serializers import UserProfileSerializer, UserProfilePhotoSerializer
import logging

logger = logging.getLogger(__name__)

class UserProfileTest(APITestCase):
    def add_user_profile(self):
        logger.debug('Adding a new person into database')
        