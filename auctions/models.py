from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listings(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    starting_bit = models.IntegerField()
    ##creator = models.ForeignKey()
    ##creator = models.TextField(max_length=100)
    def __str__(self):

        return f"{self.title, self.starting_bit, self.description}"

class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing}"




