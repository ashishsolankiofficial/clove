from rest_framework import serializers

from django.shortcuts import get_object_or_404

from team.models import Team
from user.models import User
from office.models import Office
from playable.models import BilateralMatch
from payable.models import PayableProfile, OfficeBet, UnsettledBet


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
    placed_bets = serializers.SerializerMethodField()

    class Meta:
        model = OfficeBet
        fields = ['ext_id', 'match', 'office', 'settled', 'placed_bets']
        read_only_fields = ['ext_id']

    def get_placed_bets(self, obj):
        return UnsettledBetSerializer(obj.ubets.all(), many=True).data

    def create(self, validated_data):
        user = User.objects.get(ext_id=self.context.get('request').user.ext_id)
        team = Team.objects.get(ext_id=self.context.get('request').data['placed_bets'][0]['team'])
        instance = OfficeBet.objects.create(**validated_data)
        ubet = UnsettledBet.objects.create(bet=instance, user=user, team=team, amount=self.context.get('request').data['placed_bets'][0]['amount'])
        user_profile = PayableProfile.objects.get(user=user)
        user_profile.coins = user_profile.coins - ubet.amount
        user_profile.save()
        return instance

    def update(self, instance, validated_data):
        user = User.objects.get(ext_id=self.context.get('request').user.ext_id)
        team = Team.objects.get(ext_id=self.context.get('request').data['placed_bets'][0]['team'])
        try:
            ubet = instance.ubets.get(user=user)
            ubet.team = team
            previous_bet_amount = ubet.amount
            ubet.amount = self.context.get('request').data['placed_bets'][0]['amount']
            ubet.save()
            user_profile = PayableProfile.objects.get(user=user)
            user_profile.coins = user_profile.coins - (ubet.amount - previous_bet_amount)
            user_profile.save()
        except UnsettledBet.DoesNotExist:
            ubet = UnsettledBet.objects.create(bet=instance, user=user, team=team, amount=self.context.get('request').data['placed_bets'][0]['amount'])
            user_profile = PayableProfile.objects.get(user=user)
            user_profile.coins = user_profile.coins - ubet.amount
            user_profile.save()
        return instance


class PayableProfileSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='user.display_name')

    class Meta:
        model = PayableProfile
        fields = ['display_name', 'coins']
