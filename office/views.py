from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from user.models import User
from payable.models import PayableProfile
from payable.serializer import PayableProfileSerializer


class LeaderBoardView(APIView):
    def get(self, request):
        user = User.objects.get(ext_id=request.user.ext_id)
        profile = PayableProfile.objects.filter(user__office__ext_id=user.office.ext_id)
        serializer = PayableProfileSerializer(profile, many=True)
        return Response(serializer.data)
