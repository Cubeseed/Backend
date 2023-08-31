import logging
from django.db import models
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from cubeseed.settings import COUNTRY_CODES


class Address(models.Model):
    address = models.CharField(max_length=100, verbose_name="Street address")
    address_detail = models.CharField(
        max_length=100, blank=True, verbose_name="Apartment, Suite, Unit, Box number, etc."
    )
    locality = models.CharField(max_length=100, blank=True, verbose_name="City or Town name")
    administrative_area = models.CharField(max_length=100, blank=True, verbose_name="State, Province or Region name")
    country = models.CharField(max_length=2, default="NG", verbose_name="Country 2 character ISO code. Defaults to NG")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="Postal code")
    osm_checked = models.BooleanField(default=False, verbose_name="Checked by Open Street Map API")
    osm_longitude = models.FloatField(null=True)
    osm_latitude = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            self.address + self.address_detail + ", ".join([self.locality, self.administrative_area, self.postal_code])
        )

    def resolve_location(self, address):
        geolocator = Nominatim(user_agent="cubeseed-backend")
        location = geolocator.geocode(address, country_codes=COUNTRY_CODES)
        return location

    def save(self, *args, **kwargs):
        try:
            location = self.resolve_location(
                ", ".join([self.address, self.locality, self.administrative_area, self.postal_code])
            )
            if location is None:
                # try excluding locality
                location = self.resolve_location(", ".join([self.address, self.administrative_area, self.postal_code]))
            if location is None:
                # try excluding administrative area
                location = self.resolve_location(", ".join([self.address, self.postal_code]))
            if location is None:
                # try excluding postal code
                location = self.resolve_location(", ".join([self.address, self.postal_code]))

            if location is not None:
                self.osm_checked = True
                self.osm_longitude = location.longitude
                self.osm_latitude = location.latitude
        except GeocoderTimedOut:
            logging.getLogger(__name__).warning("Nominatim geocode timed out.")

        super().save(*args, **kwargs)
