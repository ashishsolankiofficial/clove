from rest_framework import serializers
from playable.models import Sport, BilateralMatch
from payable.models import UnsettledBet
from payable.serializer import UnsettledBetSerializer
from team.serializer import TeamSerializer


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
        templates = BilateralMatch.objects.filter(tournament__sport__ext_id=obj.ext_id)
        return MatchSerializer(templates, many=True).data


class YourBetSerializer(serializers.ModelSerializer):
    teamA = TeamSerializer()
    teamB = TeamSerializer()
    tournament_name = serializers.CharField(source='tournament.name')
    ubet = serializers.SerializerMethodField()

    class Meta:
        model = BilateralMatch
        fields = ['ext_id', 'name', 'match_start_time', 'teamA', 'teamB', 'tournament_name', 'ubet']

    def get_ubet(self, obj):
        ubet = UnsettledBet.objects.get(user__ext_id=self.context.get("request").user.ext_id, bet__match__ext_id=obj.ext_id)
        return UnsettledBetSerializer(ubet).data
