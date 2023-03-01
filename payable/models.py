from django.db import models
from util.models import get_ext_id

from team.models import Team
from user.models import User
from office.models import Office
from playable.models import BilateralMatch


class PayableProfile(models.Model):
    ext_id = models.CharField(max_length=10)
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE, null=True)
    coins = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.display_name


class OfficeBet(models.Model):
    ext_id = models.CharField(max_length=10)
    match = models.ForeignKey(BilateralMatch, related_name='bet', on_delete=models.CASCADE)
    office = models.ForeignKey(Office, related_name='office_bets', on_delete=models.CASCADE)
    settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.match.name


class UnsettledBet(models.Model):
    user = models.ForeignKey(User, related_name="ubets", on_delete=models.CASCADE)
    bet = models.ForeignKey(OfficeBet, related_name="ubets", on_delete=models.CASCADE, null=True)
    team = models.ForeignKey(Team, related_name="team_bets", on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class SettledBet(models.Model):
    user = models.ForeignKey(User, related_name="sbets", on_delete=models.CASCADE)
    bet = models.ForeignKey(OfficeBet, related_name="sbets", on_delete=models.CASCADE, null=True)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
