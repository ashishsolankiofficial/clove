from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from playable.forms import TournamentForm, BilateralMatchForm, BilateralMatchWinnerForm
from playable.models import Tournament, BilateralMatch, Sport
from payable.models import SettledBet, PayableProfile, OfficeBet
from user.models import User
from datetime import datetime
from django.db.models import Sum

from playable.models import Sport, BilateralMatch
from playable.serializer import UpcommingSerializer, MatchSerializer, YourBetSerializer


class UpcommingView(APIView):
    def get(self, request):
        user = User.objects.get(ext_id=request.user.ext_id)
        sports_with_unsettled_bet = Sport.objects.filter(ext_id__in=OfficeBet.objects.filter(office=user.office, match__active=True,
                                                         settled=False).values_list('match__tournament__sport__ext_id', flat=True))
        sports_without_bet = Sport.objects.filter(ext_id__in=BilateralMatch.objects.filter(active=True, winner=None).values_list('tournament__sport__ext_id', flat=True))
        sports = sports_with_unsettled_bet | sports_without_bet
        serializer = UpcommingSerializer(sports, many=True, context={'request': request})
        return Response(serializer.data)


class MatchView(APIView):
    def get(self, request, ext_id):
        match = BilateralMatch.objects.get(ext_id=ext_id)
        serializer = MatchSerializer(match, context={'request': request})
        return Response(serializer.data)


class YourBetsView(APIView, LimitOffsetPagination):
    def get(self, request):
        match = BilateralMatch.objects.filter(bet__ubets__user__ext_id=request.user.ext_id).order_by('match_start_time')
        results = self.paginate_queryset(match, request, view=self)
        serializer = YourBetSerializer(results, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


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
    return render(request, 'playable/add_tournament.html', {'form': fm})


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
    return render(request, 'playable/add_tournament.html', {'form': fm})


def list_tournament(request):
    tournaments = Tournament.objects.filter(active=True).order_by('-created_at').values('ext_id', 'name', 'sport__name', 'created_by__display_name', 'active')
    tournament_list = {
        'tournament_list': tournaments
    }
    return render(request, 'playable/list_tournament.html', tournament_list)


def list_inactive_tournament(request):
    tournaments = Tournament.objects.filter(active=False).order_by('-created_at').values('ext_id', 'name', 'sport__name', 'created_by__display_name', 'active')
    page = request.GET.get('page', 1)
    paginator = Paginator(tournaments, 10)
    try:
        tournaments = paginator.page(page)
    except PageNotAnInteger:
        tournaments = paginator.page(1)
    except EmptyPage:
        tournaments = paginator.page(paginator.num_pages)
    tournament_list = {
        'tournament_list': tournaments
    }
    return render(request, 'playable/list_inactive_tournament.html', tournament_list)


def add_match(request, t_id):
    tournament = Tournament.objects.get(ext_id=t_id)
    if request.method == 'POST':
        fm = BilateralMatchForm(data=request.POST, tournament=tournament)
        if fm.is_valid():
            match = fm.save(commit=False)
            match.created_by = User.objects.get(ext_id=request.user.ext_id)
            match.tournament = tournament
            match.save()
            return redirect("list_match", t_id)
    else:
        fm = BilateralMatchForm(tournament=tournament)
    return render(request, 'playable/add_match.html', {'form': fm, 'tournament_id': t_id})


def edit_match(request, t_id, ext_id):
    tournament = Tournament.objects.get(ext_id=t_id)
    match = get_object_or_404(BilateralMatch, ext_id=ext_id)
    if request.method == 'POST':
        fm = BilateralMatchForm(data=request.POST, instance=match, tournament=tournament)
        if fm.is_valid():
            match = fm.save(commit=False)
            match.created_by = User.objects.get(ext_id=request.user.ext_id)
            match.tournament = Tournament.objects.get(ext_id=t_id)
            match.save()
            if not match.active:
                for office_bet in match.bet.all():
                    ubets = office_bet.ubets.all()
                    for ubet in ubets:
                        refund_amount = ubet.amount
                        sbet = SettledBet.objects.create(bet=office_bet, user=ubet.user, amount=refund_amount)
                        user_profile = PayableProfile.objects.get(user=ubet.user)
                        user_profile.coins = user_profile.coins + refund_amount
                        user_profile.save()

            return redirect("list_match", t_id)
    else:
        fm = BilateralMatchForm(instance=match, tournament=tournament)
    return render(request, 'playable/add_match.html', {'form': fm, 'tournament_id': t_id})


def list_match(request, t_id):
    tournament = Tournament.objects.get(ext_id=t_id)
    user = User.objects.get(ext_id=request.user.ext_id)
    matches = BilateralMatch.objects.filter(tournament__ext_id=t_id, active=True).order_by('-created_at').values('ext_id', 'name', 'match_start_time',
                                                                                                                 'active', 'teamA__name', 'teamB__name', 'winner__name', 'created_by__display_name')
    for match in matches:
        bet = OfficeBet.objects.filter(match__ext_id=match['ext_id'], office__ext_id=user.office.ext_id).first()
        if bet:
            if bet.settled:
                match['bet_settled'] = True
            if not bet.settled:
                match['bet_settled'] = False
        else:
            match['bet_settled'] = True
    match_list = {
        'tournament': tournament,
        'match_list': matches
    }
    return render(request, 'playable/list_match.html', match_list)


def list_inactive_match(request, t_id):
    tournament = Tournament.objects.get(ext_id=t_id)
    matches = BilateralMatch.objects.filter(tournament__ext_id=t_id, active=False).order_by('-created_at').values('ext_id', 'name', 'match_start_time',
                                                                                                                  'active', 'teamA__name', 'teamB__name', 'winner__name', 'created_by__display_name')
    page = request.GET.get('page', 1)
    paginator = Paginator(matches, 10)
    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    match_list = {
        'tournament': tournament,
        'match_list': matches
    }
    return render(request, 'playable/list_inactive_match.html', match_list)


def choose_winner(request, t_id, ext_id):
    match = get_object_or_404(BilateralMatch, ext_id=ext_id)
    if request.method == 'POST':
        if match.teamA.id == int(request.POST['winner']):
            match.winner = match.teamA
            match.save()
        if match.teamB.id == int(request.POST['winner']):
            match.winner = match.teamB
            match.save()
        if not match.bet.all().exists():
            match.active = False
            match.save()
        return redirect("list_match", t_id)
    else:
        fm = BilateralMatchWinnerForm(teams=[match.teamA.ext_id, match.teamB.ext_id])
    return render(request, 'playable/choose_winner.html', {'form': fm, 'tournament_id': t_id})


def distribute_rewards(request, t_id, ext_id):
    match = get_object_or_404(BilateralMatch, ext_id=ext_id)
    user = User.objects.get(ext_id=request.user.ext_id)
    office_bet = match.bet.filter(office__ext_id=user.office.ext_id).first()
    if office_bet:
        ubets = office_bet.ubets.all()
        team_a_ubets = ubets.filter(team__ext_id=match.teamA.ext_id)
        team_b_ubets = ubets.filter(team__ext_id=match.teamB.ext_id)
        team_a_total = 0
        team_b_total = 0
        if team_a_ubets:
            team_a_total = team_a_ubets.aggregate(Sum('amount'))['amount__sum']
        if team_b_ubets:
            team_b_total = team_b_ubets.aggregate(Sum('amount'))['amount__sum']
        if match.teamA.ext_id == match.winner.ext_id:
            for ubet in team_a_ubets:
                win_amount = ubet.amount + (team_b_total * ubet.amount/team_a_total)
                sbet = SettledBet.objects.create(bet=office_bet, user=ubet.user, amount=win_amount)
                user_profile = PayableProfile.objects.get(user=ubet.user)
                user_profile.coins = user_profile.coins + sbet.amount
                user_profile.save()
            if not team_a_ubets:
                for ubet in team_b_ubets:
                    refund_amount = ubet.amount
                    sbet = SettledBet.objects.create(bet=office_bet, user=ubet.user, amount=refund_amount)
                    user_profile = PayableProfile.objects.get(user=ubet.user)
                    user_profile.coins = user_profile.coins + refund_amount
                    user_profile.save()
        if match.teamB.ext_id == match.winner.ext_id:
            for ubet in team_b_ubets:
                win_amount = ubet.amount + (team_a_total * ubet.amount/team_b_total)
                sbet = SettledBet.objects.create(bet=office_bet, user=ubet.user, amount=win_amount)
                user_profile = PayableProfile.objects.get(user=ubet.user)
                user_profile.coins = user_profile.coins + sbet.amount
                user_profile.save()
            if not team_b_ubets:
                for ubet in team_a_ubets:
                    refund_amount = ubet.amount
                    sbet = SettledBet.objects.create(bet=office_bet, user=ubet.user, amount=refund_amount)
                    user_profile = PayableProfile.objects.get(user=ubet.user)
                    user_profile.coins = user_profile.coins + refund_amount
                    user_profile.save()
        office_bet.settled = True
        office_bet.save()
    if not match.bet.filter(settled=False).exists():
        match.active = False
        match.save()
    return redirect("list_match", t_id)
