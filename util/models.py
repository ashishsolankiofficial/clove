from django.db import models
import random

# Create your models here.


class Country(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


def get_ext_id():
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(10))
