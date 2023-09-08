"""Model for Cluster"""
from django.db import models
from cubeseed.commodity.models import Commodity

# Create your models here.
class Cluster(models.Model):
    """
    Cluster Model
    """
    cluster_name = models.CharField(max_length=50)
    local_government_name = models.CharField(max_length=50)
    commodity = models.ForeignKey(Commodity, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.cluster_name
