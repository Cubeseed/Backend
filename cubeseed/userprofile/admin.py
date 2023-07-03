# Register your models here.
from django.contrib import admin
from cubeseed.userprofile.models import UserProfile, UserProfilePhoto

admin.site.register(UserProfile)
admin.site.register(UserProfilePhoto)
