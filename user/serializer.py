from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    ...

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['ext_id'] = user.ext_id
        # del token['user_id']
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
