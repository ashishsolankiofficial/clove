from django import forms
from user.models import User

# Create the form class.


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'display_name', 'office']
