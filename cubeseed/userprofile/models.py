from django.db import models
from django.core.files.storage import default_storage

# User Profile Model for Cubeseed
class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.full_name + " - " + self.user.username + " - " + self.user.email
    

def upload_user_profile_image(instance, filename):
    image_name = "user_profile_images/%s" % (instance.user_profile.user.id)
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