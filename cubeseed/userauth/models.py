# from django.db import models

# Create your models here.
from django.db import models


class Course(models.Model):
    objects = None
    link = models.CharField(max_length=100000, blank=False)
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=100, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
