from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listings(models.Model):
    ##id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    starting_bit = models.IntegerField()
    image_URL = models.URLField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.TextField(max_length=100, default="Others")
    closed = models.BooleanField(default=False)
    def __str__(self):

        return f"{self.title, self.starting_bit, self.description,self.category,self.closed}"

class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing}"
class comments(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user.username,self.comment,self.listing.title}"

class bids(models.Model):
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)
    current_bid = models.IntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_bids')
    current_winner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True,
                                      related_name='winner_bids')


def __str__(self):
        return f"{self.current_bid}"





