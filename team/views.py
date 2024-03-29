from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from user.models import User
from team.models import Team
from team.forms import TeamForm


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
    return render(request, 'team/add_team.html', {'form': fm})


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
    return render(request, 'playable/add_tournament.html', {'form': fm})


def list_team(request):
    teams = Team.objects.filter(active=True).order_by('-created_at').values('ext_id', 'type', 'name', 'country__name', 'created_by__display_name', 'sport__name', 'active')
    page = request.GET.get('page', 1)
    paginator = Paginator(teams, 10)
    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        teams = paginator.page(1)
    except EmptyPage:
        teams = paginator.page(paginator.num_pages)
    team_list = {
        'team_list': teams
    }
    return render(request, 'team/list_team.html', team_list)


def list_inactive_team(request):
    teams = Team.objects.filter(active=False).order_by('-created_at').values('ext_id', 'type', 'name', 'country__name', 'created_by__display_name', 'sport__name', 'active')
    page = request.GET.get('page', 1)
    paginator = Paginator(teams, 10)
    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        teams = paginator.page(1)
    except EmptyPage:
        teams = paginator.page(paginator.num_pages)
    team_list = {
        'team_list': teams
    }
    return render(request, 'team/list_inactive_team.html', team_list)
