from django.db import models
from util.models import get_ext_id


class Office(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    address = models.TextField()

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    ext_id = models.CharField(max_length=10)
    task = models.TextField()
    active = models.BooleanField(default=True)
    office = models.ForeignKey(Office, related_name='tasks', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)
