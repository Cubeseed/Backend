"""Register models for admin site"""
from django.contrib import admin
from .models import BusinessProfile

admin.site.register(BusinessProfile)
