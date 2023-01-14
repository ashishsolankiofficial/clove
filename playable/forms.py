from django import forms
from playable.models import Tournament, BilateralMatch


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'


class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        exclude = ['ext_id', 'created_by']


class BilateralMatchForm(forms.ModelForm):

    class Meta:
        model = BilateralMatch
        exclude = ['ext_id', 'created_by', 'winner', 'tournament']
