"""Room related models"""
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

# Room model
class Room(models.Model):
    """
    Room Model
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        """
        Gets count of users that are online in a room
        """
        return self.online.count()
    
    def join(self, user):
        """
        Adds a user to the online list of a room

        Parameters:
        user: User
            The user to add to the online list of a room
        """
        self.online.add(user)
        self.save()

    def leave(self, user):
        """
        Removes a user from the online list of a room

        Parameters:
        user: User
            The user to remove from the online list of a room
        """
        self.online.remove(user)
        self.save()

    
# Message Model
class Message(models.Model):
    """
    Message Model
    """
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='messages_from_me', on_delete=models.CASCADE, null=True)
    to_user = models.ForeignKey(User, related_name='messages_to_me', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    multimedia_url = models.TextField(null=True, blank=True, default=None)
    multimedia_save_location = models.TextField(null=True, blank=True, default=None)
    file_identifier = models.TextField(null=True, blank=True, default=None)
    multimedia_url_expiration = models.TextField(null=True, blank=True, default=None)
    date_added = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ('date_added',)
