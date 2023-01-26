from django.shortcuts import get_object_or_404
from rest_framework import serializers
from payable.models import PayableProfile, BilateralBet, UnsettledBet
from office.models import Office
from playable.models import BilateralMatch
from user.models import User
from team.models import Team


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayableProfile
        fields = ['coins']


class UnsettledBetSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    team_ext_id = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()

    class Meta:
        model = UnsettledBet
        fields = ['user_name', 'user_id', 'amount', 'team_ext_id', 'team_name']

    def get_user_name(self, obj):
        return obj.user.display_name

    def get_user_id(self, obj):
        return obj.user.ext_id

    def get_team_ext_id(self, obj):
        return obj.team.ext_id

    def get_team_name(self, obj):
        return obj.team.name


class BetSerializer(serializers.ModelSerializer):
    match = serializers.SlugRelatedField(slug_field='ext_id', queryset=BilateralMatch.objects.all())
    office = serializers.SlugRelatedField(slug_field='ext_id', queryset=Office.objects.all())
    placed_bets = UnsettledBetSerializer(many=True)

    class Meta:
        model = BilateralBet
        fields = ['ext_id', 'match', 'office', 'settled', 'placed_bets']
        read_only_fields = ['ext_id', 'placed_bets']

    def create(self, validated_data):
        user = User.objects.get(ext_id=self.context.get('request').user.ext_id)
        team = Team.objects.get(ext_id=self.context.get('request').data['placed_bets'][0]['team'])
        ubet = UnsettledBet.objects.create(user=user, team=team, amount=self.context.get('request').data['placed_bets'][0]['amount'])
        instance = BilateralBet.objects.create(**validated_data)
        instance.placed_bets.add(ubet)
        return instance

    def update(self, instance, validated_data):
        user = User.objects.get(ext_id=self.context.get('request').user.ext_id)
        team = Team.objects.get(ext_id=self.context.get('request').data['placed_bets'][0]['team'])
        try:
            ubet = instance.placed_bets.get(user=user)
            ubet.team = team
            ubet.amount = self.context.get('request').data['placed_bets'][0]['amount']
            ubet.save()
        except:
            ubet = UnsettledBet.objects.create(user=user, team=team, amount=self.context.get('request').data['placed_bets'][0]['amount'])
            instance.placed_bets.add(ubet)
            instance.save()
        return instance
