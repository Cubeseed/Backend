"""Farm related models"""
from django.db import models
from cubeseed.businessprofile.models import BusinessProfile
from cubeseed.cluster.models import Cluster
from cubeseed.address.models import Address
from cubeseed.commodity.models import Commodity

class Farm(models.Model):
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Size in Hectares")
    # The field below will be changed back to OneToOneField
    farm_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    # A farm can exist without a cluster, hence it
    # is set to null upon deletion of a cluster
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True, related_name="farms")
    commodity = models.ForeignKey(Commodity, on_delete=models.SET_NULL, null=True, related_name="farms")

