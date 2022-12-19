from django.db import models
from django.contrib.auth.models import AbstractUser
from util.models import get_ext_id

# Create your models here.


class User(AbstractUser):
    ext_id = models.CharField(max_length=10)
    email = models.EmailField(max_lenght=254, unique=True)
    display_name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'display_name']

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.email)
