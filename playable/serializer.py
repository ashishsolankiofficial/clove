from rest_framework import serializers
from playable.models import Sport, BilateralMatch
from payable.models import UnsettledBet
from payable.serializer import UnsettledBetSerializer
from team.serializer import TeamSerializer
from user.models import User


class MatchSerializer(serializers.ModelSerializer):
    teamA = TeamSerializer()
    teamB = TeamSerializer()
    tournament_name = serializers.CharField(source='tournament.name')
    bet_ext_id = serializers.SerializerMethodField()

    class Meta:
        model = BilateralMatch
        fields = ['ext_id', 'name', 'match_start_time', 'teamA', 'teamB', 'tournament_name', 'bet_ext_id']

    def get_bet_ext_id(self, obj):
        if (obj.bet.last()):
            return obj.bet.last().ext_id
        else:
            return None


class UpcommingSerializer(serializers.ModelSerializer):
    match = serializers.SerializerMethodField()

    class Meta:
        model = Sport
        fields = ['ext_id', 'name', 'match']

    def get_match(self, obj):
        matches = BilateralMatch.objects.filter(tournament__sport__ext_id=obj.ext_id, active=True)
        return MatchSerializer(matches, many=True).data


class YourBetSerializer(serializers.ModelSerializer):
    teamA = TeamSerializer()
    teamB = TeamSerializer()
    winner_ext_id = serializers.SerializerMethodField()
    tournament_name = serializers.CharField(source='tournament.name')
    ubet = serializers.SerializerMethodField()
    bet_settled = serializers.SerializerMethodField()
    refund = serializers.SerializerMethodField()

    class Meta:
        model = BilateralMatch
        fields = ['ext_id', 'name', 'match_start_time', 'teamA', 'teamB', 'tournament_name', 'ubet', 'bet_settled', 'winner_ext_id', 'refund']

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
        return False if len(obj.bet.get(office__ext_id=office_ext_id).ubets.all().values('team__ext_id').distinct()) == 2 else True
