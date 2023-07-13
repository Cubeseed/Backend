"""Farm related models"""
from django.db import models
from cubeseed.businessprofile.models import BusinessProfile

class Farm(models.Model):
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Size in Hectares")
