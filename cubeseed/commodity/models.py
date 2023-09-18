"""Model for Commodity"""
from django.db import models

# Create your models here.
class Commodity(models.Model):
    """
    Commodity Model
    """
    commodity_name = models.CharField(max_length=50)

    def __str__(self):
        return self.commodity_name