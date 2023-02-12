from django.db import models
from django.contrib.auth.models import AbstractUser
from util.models import get_ext_id
from office.models import Office
from .manager import UserManager


# Create your models here.


class User(AbstractUser):
    ext_id = models.CharField(max_length=10)
    email = models.EmailField(max_length=254, unique=True)
    display_name = models.CharField(max_length=50, unique=True)
    can_play = models.BooleanField(default=True)
    office = models.ForeignKey(Office, related_name='employees', on_delete=models.CASCADE, null=True)
    office_admin = models.BooleanField(default=False)
    super_admin = models.BooleanField(default=False)
    username = None
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'display_name']

    objects = UserManager()

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)
