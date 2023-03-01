from django.db import models
from util.models import get_ext_id

from user.models import User
from team.models import Team


class Sport(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)


class Tournament(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    sport = models.ForeignKey(Sport, related_name='tournaments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='tournaments', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BilateralMatch(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    match_start_time = models.DateTimeField()
    tournament = models.ForeignKey(Tournament, related_name='tournament_matches', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    teamA = models.ForeignKey(Team, related_name='ateam_matches', on_delete=models.CASCADE)
    teamB = models.ForeignKey(Team, related_name='bteam_matches', on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, related_name='won_matches', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, related_name='bilateral_matches', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
