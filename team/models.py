from django.db import models
from util.models import get_ext_id

from user.models import User
from util.models import Country


class Team(models.Model):

    TYPE_CHOICES = (
        ("N", "National"),
        ("C", "Club"),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default="C")
    ext_id = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='team', on_delete=models.CASCADE)
    sport = models.ForeignKey("playable.Sport", related_name="teams", on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name='bilateralmatch', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)
