from django.db import models
from playable.models import Sport
from util.models import get_ext_id


class Team(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100, unique=True)
    sport = models.ForeignKey(Sport, related_name='tournament', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)
