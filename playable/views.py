from django.shortcuts import render, redirect, get_object_or_404
from playable.forms import TournamentForm
from playable.models import Tournament
from user.models import User


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
