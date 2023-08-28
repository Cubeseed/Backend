from django.db import models
from geopy.geocoders import Nominatim
from cubeseed.settings import COUNTRY_CODES

class Address(models.Model):
    # user provided fields, may be nonsense
    address = models.CharField(max_length=100, verbose_name="Street address")
    address_detail = models.CharField(max_length=100, verbose_name="Apartment, Suite, Unit, Box number, etc.")
    locality = models.CharField(max_length=100, verbose_name="City or Town name")
    administrative_area = models.CharField(max_length=50, verbose_name="State, Province or Region name")
    country = models.CharField(max_length=2, default="NG", verbose_name="Country 2 character ISO code. Defaults to NG")
    postal_code = models.CharField(max_length=10, verbose_name="Postal code")
    osm_checked = models.BooleanField(default=False, verbose_name="Checked by Open Street Map API")
    osm_longitude = models.FloatField(null=True)
    osm_latitude = models.FloatField(null=True)

    def __str__(self):
        return (
            self.address + self.address_detail + ", ".join([self.locality, self.administrative_area, self.postal_code])
        )

    def save(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="cubeseed-backend")
        location = geolocator.geocode(
            ", ".join([self.address, self.locality, self.administrative_area, self.postal_code]),
            country_codes = COUNTRY_CODES
        )
        if location is not None:
            self.osm_checked = True
            self.osm_longitude = location.longitude
            self.osm_latitude = location.latitude
        super().save(*args, **kwargs)
