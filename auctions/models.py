from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    starting_bit = models.IntegerField()

    def __str__(self):
        return f"{self.title, self.starting_bit, self.description}"




