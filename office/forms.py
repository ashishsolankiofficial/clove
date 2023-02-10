from django import forms
from office.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['ext_id', 'office']
