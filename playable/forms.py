from django import forms
from playable.models import Tournament


class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        exclude = ['ext_id', 'created_by']
