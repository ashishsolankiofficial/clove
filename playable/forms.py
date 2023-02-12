from django import forms
from django.core.exceptions import ValidationError
from playable.models import Tournament, BilateralMatch
from team.models import Team


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        exclude = ['ext_id', 'created_by']


class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'


class BilateralMatchForm(forms.ModelForm):
    class Meta:
        model = BilateralMatch
        exclude = ['ext_id', 'created_by', 'winner', 'tournament']
        widgets = {
            'match_start_time': DateTimeInput()
        }

    def __init__(self, tournament=None, *args, **kwargs):
        super(BilateralMatchForm, self).__init__(*args, **kwargs)
        if tournament:
            self.fields['teamA'].queryset = Team.objects.filter(sport=tournament.sport, active=True)
            self.fields['teamB'].queryset = Team.objects.filter(sport=tournament.sport, active=True)

    def clean(self):
        team_a = self.cleaned_data['teamA']
        team_b = self.cleaned_data['teamB']
        if team_a == team_b:
            raise ValidationError("Team A & Team B cannot be same")
        return self.cleaned_data

class BilateralMatchWinnerForm(forms.ModelForm):
    class Meta:
        model = BilateralMatch
        fields = ['winner', ]

    def __init__(self, teams, *args, **kwargs):
        super(BilateralMatchWinnerForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['winner'].queryset = Team.objects.filter(ext_id__in=teams)
