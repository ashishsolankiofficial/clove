from django import forms
from team.models import Team


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        exclude = ['ext_id', 'created_by']
