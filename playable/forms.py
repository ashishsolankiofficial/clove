from django import forms
from playable.models import Tournament, BilateralMatch
from django.contrib.admin.widgets import AdminSplitDateTime


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
