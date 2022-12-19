from django.db import models
from util.models import get_ext_id
from user.models import User


class Office(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    address = models.TextField()
    administrator = models.ForeignKey(User, related_name='office', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)
