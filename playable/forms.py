import pytz
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from playable.models import Tournament, BilateralMatch
from team.models import Team


class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        exclude = ['ext_id', 'created_by']


class BilateralMatchForm(forms.ModelForm):
    class Meta:
        model = BilateralMatch
        exclude = ['ext_id', 'created_by', 'winner', 'tournament']
        widgets = {
            'match_start_time': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'type': 'datetime-local'})
        }

    def __init__(self, tournament=None, *args, **kwargs):
        super(BilateralMatchForm, self).__init__(*args, **kwargs)
        if tournament:
            self.fields['teamA'].queryset = Team.objects.filter(sport=tournament.sport, active=True)
            self.fields['teamB'].queryset = Team.objects.filter(sport=tournament.sport, active=True)

    def clean(self):
        cleaned_data = super().clean()
        if 'teamA' in cleaned_data and 'teamB' in cleaned_data:
            if cleaned_data['teamA'] == cleaned_data['teamB']:
                raise ValidationError("Team A & Team B cannot be same")


class BilateralMatchWinnerForm(forms.ModelForm):
    class Meta:
        model = BilateralMatch
        fields = ['winner', ]

    def __init__(self, teams, *args, **kwargs):
        super(BilateralMatchWinnerForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['winner'].queryset = Team.objects.filter(ext_id__in=teams)
