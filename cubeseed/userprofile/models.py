from django.db import models

def upload_user_profile_image(instance, filename):
    return "user_profile_images/%s" % (instance.user.id)

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
    picture = models.ImageField(upload_to=upload_user_profile_image, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.full_name + " - " + self.user.username + " - " + self.user.email