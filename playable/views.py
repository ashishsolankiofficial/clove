from django.shortcuts import render, redirect, get_object_or_404
from playable.forms import TournamentForm, BilateralMatchForm
from playable.models import Tournament, BilateralMatch
from user.models import User
from datetime import datetime


def add_tournament(request):
    if request.method == 'POST':
        fm = TournamentForm(request.POST)
        if fm.is_valid():
            tournament = fm.save(commit=False)
            tournament.created_by = User.objects.get(ext_id=request.user.ext_id)
            tournament.save()
            return redirect("list_tournament")
    else:
        fm = TournamentForm()
    return render(request, 'add_tournament.html', {'form': fm})


def edit_tournament(request, ext_id):
    tournament = get_object_or_404(Tournament, ext_id=ext_id)
    if request.method == 'POST':
        fm = TournamentForm(request.POST, instance=tournament)
        if fm.is_valid():
            tournament = fm.save(commit=False)
            tournament.created_by = User.objects.get(ext_id=request.user.ext_id)
            tournament.save()
            return redirect("list_tournament")
    else:
        fm = TournamentForm(instance=tournament)
    return render(request, 'add_tournament.html', {'form': fm})


def list_tournament(request):
    tournaments = Tournament.objects.all().values('ext_id', 'name', 'sport__name', 'created_by__display_name', 'active')
    tournament_list = {
        'tournament_list': tournaments
    }
    return render(request, 'list_tournament.html', tournament_list)


def add_match(request, t_id):
    if request.method == 'POST':
        fm = BilateralMatchForm(request.POST)
        if fm.is_valid():
            match = fm.save(commit=False)
            match.created_by = User.objects.get(ext_id=request.user.ext_id)
            match.tournament = Tournament.objects.get(ext_id=t_id)
            match.save()
            return redirect("list_match", t_id)
    else:
        fm = BilateralMatchForm()
    return render(request, 'add_match.html', {'form': fm, 'tournament_id': t_id})


def edit_match(request, t_id, ext_id):
    match = get_object_or_404(BilateralMatch, ext_id=ext_id)
    if request.method == 'POST':
        fm = BilateralMatchForm(request.POST, instance=match)
        if fm.is_valid():
            match = fm.save(commit=False)
            match.created_by = User.objects.get(ext_id=request.user.ext_id)
            match.tournament = Tournament.objects.get(ext_id=t_id)
            match.save()
            return redirect("list_match", t_id)
    else:
        fm = BilateralMatchForm(instance=match)
    return render(request, 'add_match.html', {'form': fm, 'tournament_id': t_id})


def list_match(request, t_id):
    tournament = Tournament.objects.get(ext_id=t_id)
    matches = BilateralMatch.objects.filter(tournament__ext_id=t_id).values('ext_id', 'name', 'match_start_time', 'active', 'teamA__name', 'teamB__name', 'winner', 'created_by__display_name')
    match_list = {
        'tournament': tournament,
        'match_list': matches
    }
    return render(request, 'list_match.html', match_list)
