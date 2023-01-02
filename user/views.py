from django.shortcuts import render
from user.forms import UserForm


def user_registration(request):

    fm = UserForm()

    return render(request, 'user_registration.html', {'form': fm})
