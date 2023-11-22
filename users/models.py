from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)

    def follow(self, profile):
        self.following.add(profile)

    def unfollow(self, profile):
        self.following.remove(profile)


    def __str__(self):
        return self.user.username  # Return a string representation of the profile

class LiveEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.name
