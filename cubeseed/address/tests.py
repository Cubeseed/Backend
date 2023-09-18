from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Address


class AddressModelTest(TestCase):
    def test_ng_address_1(self):
        addr = Address()
        addr.address = "42, Olowu Street"
        addr.save()
        self.assertEqual(addr.osm_checked, True, msg="OSM Check failed")
        #self.assertAlmostEqual(addr.osm_latitude, 6.5963104, msg="wrong latitude")
        #self.assertAlmostEqual(addr.osm_longitude, 3.3438925, msg="wrong longitude")

    def test_fake_address_1(self):
        addr = Address()
        addr.address = "5555, Fake Street"
        addr.save()
        self.assertEqual(addr.osm_checked, False, msg="OSM Check failed: " + str(addr))


User = get_user_model()


class AddressAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user.is_active = True
        self.user.groups.add(Group.objects.get(name="farmer"))
        self.user.save()
        self.url = reverse("user-detail", kwargs={"pk": self.user.pk})

    def authenticate(self):
        token_response = self.client.post(
            reverse("token_obtain_pair"), {"username": "testuser", "password": "testpassword"}
        )
        access_token = token_response.data["access"]
        # refresh_token = token_response.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_create_address(self):
        addresses = [
            {
                "address": "979 Saka Jojo Street",
                "address_detail": "",
                "locality": "Victoria",
                "administrative_area": "Lagos",
                "country": "NG",
                "postal_code": "",
                "local_government_area": "Eti Osa",
            },
            {
                "address": "1075 Diplomatic Drive",
                "address_detail": "",
                "locality": "Central District Area",
                "administrative_area": "Abuja",
                "country": "NG",
                "postal_code": "900103",
                "local_government_area": "Municipal Area Council",
            },
            {
                "address": "2 Walter Carrington Crescent",
                "address_detail": "",
                "locality": "Victoria Island",
                "administrative_area": "Lagos",
                "country": "NG",
                "postal_code": "",
                "local_government_area": "Eti Osa",
            },
        ]
        self.authenticate()
        for address in addresses:
            response = self.client.post(reverse("address-list"), format="json", data=address)
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                msg=f"Failed to create address: ${response.data} : ${self.user} : for address: ${address}",
            )
            self.assertEqual(response.data["osm_checked"], True, msg="OSM Check failed")
