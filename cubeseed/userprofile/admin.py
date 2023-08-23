# Register your models here.
from django.contrib import admin
from cubeseed.userprofile.models import UserProfile, UserProfilePhoto, FarmerProfile

admin.site.register(UserProfile)
admin.site.register(UserProfilePhoto)
admin.site.register(FarmerProfile)
