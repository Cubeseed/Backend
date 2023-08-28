from django.test import TestCase
from .models import Address

class AddressTest(TestCase):
    def test_ng_address_1(self):
        addr = Address()
        addr.address = "42, Olowu Street"
        addr.save()
        self.assertEqual(addr.osm_checked, True, msg= "OSM Check failed")
        self.assertAlmostEqual(addr.osm_latitude, 6.5963104, msg="wrong latitude")
        self.assertAlmostEqual(addr.osm_longitude, 3.3438925, msg="wrong longitude")

    def test_fake_address_1(self):
        addr = Address()
        addr.address = "5555, Fake Street"
        addr.save()
        self.assertEqual(addr.osm_checked, False, msg= "OSM Check failed: " + str(addr))

