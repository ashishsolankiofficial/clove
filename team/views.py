from django.shortcuts import render


def add_team(request):
    return render(request, 'add_team.html')


def list_team(request):
    return render(request, 'list_team.html')
