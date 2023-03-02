from rest_framework import serializers

from user.models import User
from team.serializer import TeamSerializer
from playable.models import Sport, BilateralMatch
from payable.models import UnsettledBet, OfficeBet
from payable.serializer import UnsettledBetSerializer


class MatchSerializer(serializers.ModelSerializer):
    teamA = TeamSerializer()
    teamB = TeamSerializer()
    tournament_name = serializers.CharField(source='tournament.name')
    sport_name = serializers.CharField(source='tournament.sport.name')
    bet_ext_id = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()

    class Meta:
        model = BilateralMatch
        fields = ['ext_id', 'name', 'match_start_time', 'teamA', 'teamB', 'tournament_name', 'bet_ext_id', 'winner', 'sport_name']

    def get_bet_ext_id(self, obj):
        office_ext_id = User.objects.get(ext_id=self.context.get("request").user.ext_id).office.ext_id
        return obj.bet.get(office__ext_id=office_ext_id).ext_id if obj.bet.filter(office__ext_id=office_ext_id).first() else None

    def get_winner(self, obj):
        return obj.winner.name if obj.winner else None


class UpcommingSerializer(serializers.ModelSerializer):
    match = serializers.SerializerMethodField()

    class Meta:
        model = Sport
        fields = ['ext_id', 'name', 'match']

    def get_match(self, obj):
        unsettled_office_bet_ids = OfficeBet.objects.filter(settled=False, office=User.objects.get(ext_id=self.context.get("request").user.ext_id).office).values_list('ext_id', flat=True)
        match_with_unsettled_bets = BilateralMatch.objects.filter(tournament__sport__ext_id=obj.ext_id, active=True, bet__ext_id__in=unsettled_office_bet_ids)
        match_with_no_bet = BilateralMatch.objects.filter(tournament__sport__ext_id=obj.ext_id, active=True).exclude(
            bet__office=User.objects.get(ext_id=self.context.get("request").user.ext_id).office)
        matches = match_with_unsettled_bets | match_with_no_bet
        return MatchSerializer(matches.order_by('match_start_time'), many=True, context=self.context).data


class YourBetSerializer(serializers.ModelSerializer):
    teamA = TeamSerializer()
    teamB = TeamSerializer()
    winner_ext_id = serializers.SerializerMethodField()
    tournament_name = serializers.CharField(source='tournament.name')
    ubet = serializers.SerializerMethodField()
    bet_settled = serializers.SerializerMethodField()
    win_amount = serializers.SerializerMethodField()
    refund = serializers.SerializerMethodField()

    class Meta:
        model = BilateralMatch
        fields = ['ext_id', 'name', 'match_start_time', 'teamA', 'teamB', 'tournament_name', 'ubet', 'bet_settled', 'winner_ext_id', 'refund', 'win_amount']

    def get_winner_ext_id(self, obj):
        return obj.winner.ext_id if obj.winner else None

    def get_ubet(self, obj):
        ubet = UnsettledBet.objects.get(user__ext_id=self.context.get("request").user.ext_id, bet__match__ext_id=obj.ext_id)
        return UnsettledBetSerializer(ubet).data

    def get_bet_settled(self, obj):
        office_ext_id = User.objects.get(ext_id=self.context.get("request").user.ext_id).office.ext_id
        return obj.bet.get(office__ext_id=office_ext_id).settled

    def get_refund(self, obj):
        office_ext_id = User.objects.get(ext_id=self.context.get("request").user.ext_id).office.ext_id
        if obj.active is False:
            if False in obj.bet.all().values_list('settled', flat=True):
                return True
        office_bet = obj.bet.get(office__ext_id=office_ext_id)
        if office_bet.settled is True:
            if len(office_bet.ubets.all().values('team__ext_id').distinct()) == 2:
                return False
            else:
                return True
        else:
            return False

    def get_win_amount(self, obj):
        user = User.objects.get(ext_id=self.context.get("request").user.ext_id)
        sbet = obj.bet.get(office=user.office).sbets.filter(user=user).first()
        ubet = obj.bet.get(office=user.office).ubets.filter(user=user).first()
        return sbet.amount - ubet.amount if sbet else None
