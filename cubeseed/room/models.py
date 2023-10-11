from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Room model
class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()
    
    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    # def __str__(self):
    #     return "{} ({})".format(self.name, self.get_online_count())
    
# # Conversation Model
# class Converation(models.Model):
#     name = models.CharField(max_length=128)
#     online = models.ManyToManyField(to=User, blank=True)

#     def get_online_count(self):
#         return self.online.count()
    
#     def join(self, user):
#         self.online.add(user)
#         self.save()

#     def leave(self, user):
#         self.online.remove(user)
#         self.save()

#     def __str__(self):
#         return "{} ({})".format(self.name, self.get_online_count())
    
# Message Model
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    # user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='messages_from_me', on_delete=models.CASCADE, null=True)
    to_user = models.ForeignKey(User, related_name='messages_to_me', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    # def __str__(self):
    #     return "From {} to {}: {} [{}]".format(self.from_user.username, self.to_user.username, self.content, self.date_added)

    class Meta:
        ordering = ('date_added',)
