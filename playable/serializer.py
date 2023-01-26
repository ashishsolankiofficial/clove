from rest_framework import serializers
from playable.models import Sport, BilateralMatch
from team.serializer import TeamSerializer


class MatchSerializer(serializers.ModelSerializer):
    teamA = TeamSerializer()
    teamB = TeamSerializer()
    tournament_name = serializers.CharField(source='tournament.name')

    class Meta:
        model = BilateralMatch
        fields = ['ext_id', 'name', 'match_start_time', 'teamA', 'teamB', 'tournament_name']


class UpcommingSerializer(serializers.ModelSerializer):
    match = serializers.SerializerMethodField()

    class Meta:
        model = Sport
        fields = ['ext_id', 'name', 'match']

    def get_match(self, obj):
        templates = BilateralMatch.objects.filter(tournament__sport__ext_id=obj.ext_id)
        return MatchSerializer(templates, many=True).data
