from django.db import models
import random

# Create your models here.


def get_ext_id():
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(10))
