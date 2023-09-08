"""Farm related models"""
from django.db import models
from cubeseed.businessprofile.models import BusinessProfile
from cubeseed.cluster.models import Cluster
from cubeseed.address.models import Address
from cubeseed.commodity.models import Commodity

class Farm(models.Model):
    """
    Farm Model
    """
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Size in Hectares")
    # An address can only belong to one farm
    # and a farm can only have one address
    farm_address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    # A farm is assigned to a cluster after approval
    # hence it should initally be able to exist without 
    # a cluster
    cluster = models.ForeignKey(Cluster, on_delete=models.SET_NULL, null=True, related_name="farms", default=None)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, related_name="farms")

