from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from user.models import User
from payable.serializer import CoinSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    coins = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['ext_id', 'first_name', 'last_name', 'email', 'display_name', 'coins']
        read_only_fields = ('email', 'ext_id', 'coins')

    def get_coins(self, obj):
        return obj.profile.first().coins


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    ...

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['ext_id'] = user.ext_id
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
