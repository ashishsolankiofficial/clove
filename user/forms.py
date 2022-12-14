from django import forms
from user.models import User

# Create the form class.


class AdminForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)  # Required
    last_name = forms.CharField(max_length=50)  # Required

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'display_name', 'office']


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'display_name']
