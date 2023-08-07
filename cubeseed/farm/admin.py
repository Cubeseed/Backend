"""Register models for admin site"""
from django.contrib import admin
from .models import Farm

admin.site.register(Farm)
