"""Model for Cluster"""
from django.db import models

# Create your models here.
class Cluster(models.Model):
    cluster_name = models.CharField(max_length=50)
    local_government_name = models.CharField(max_length=50)

    def __str__(self):
        return self.clustername
