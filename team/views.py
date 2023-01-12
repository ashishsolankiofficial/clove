from django.shortcuts import render, redirect, get_object_or_404
from team.forms import TeamForm
from team.models import Team
from user.models import User


def add_team(request):
    if request.method == 'POST':
        fm = TeamForm(request.POST)
        if fm.is_valid():
            team = fm.save(commit=False)
            team.created_by = User.objects.get(ext_id=request.user.ext_id)
            team.save()
            return redirect('list_team')
    else:
        fm = TeamForm()
    return render(request, 'add_team.html', {'form': fm})


def edit_team(request, ext_id):
    team = get_object_or_404(Team, ext_id=ext_id)
    if request.method == 'POST':
        fm = TeamForm(request.POST, instance=team)
        if fm.is_valid():
            team = fm.save(commit=False)
            team.created_by = User.objects.get(ext_id=request.user.ext_id)
            team.save()
            return redirect("list_team")
    else:
        fm = TeamForm(instance=team)
    return render(request, 'add_tournament.html', {'form': fm})


def list_team(request):
    teams = Team.objects.all().values('ext_id', 'type', 'name', 'country__name', 'created_by__display_name', 'active')
    team_list = {
        'team_list': teams
    }
    return render(request, 'list_team.html', team_list)
