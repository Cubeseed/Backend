from django.db import models
from django.core.files.storage import default_storage
from django.conf import settings
from cubeseed.address.models import Address


# User Profile Model for Cubeseed
class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    about_me = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name + " - " + self.user.username + " - " + self.user.email


def upload_user_profile_image(instance, filename):
    image_name = f"user_profile_images/{instance.user_profile.user.id}"
    default_storage.delete(image_name)
    return image_name


class UserProfilePhoto(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=upload_user_profile_image, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_profile.user.username + " profile photo"

    def delete(self):
        self.picture.delete()
        super().delete()


class FarmerProfile(models.Model):
    REVIEW_STATUSES = (("P", "PENDING"), ("R", "REJECTED"), ("A", "APPROVED"))
    review_status = models.CharField(max_length=1, choices=REVIEW_STATUSES, default="P")
    reviewed_by = models.OneToOneField(
        UserProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name="reviewed_farmers"
    )
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
