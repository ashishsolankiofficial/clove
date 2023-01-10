from django.db import models
from user.models import User
from util.models import get_ext_id


class Sport(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)


class Tournament(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100, unique=True)
    sport = models.ForeignKey(Sport, related_name='tournament', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)


class BilateralMatch(models.Manager):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, related_name='bilateralmatch', on_delete=models.CASCADE)
    teamA = models.ForeignKey(Team, related_name='bilateralmatch', on_delete=models.CASCADE)
    teamB = models.ForeignKey(Team, related_name='bilateralmatch', on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, related_name='bilateralmatch', on_delete=models.CASCADE, null=True)
    match_start_time = models.DateTimeField(blank=False, null=False)
    tournament = models.ForeignKey(Tournament, related_name='bilateralmatch', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)
