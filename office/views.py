from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from payable.models import PayableProfile
from payable.serializer import PayableProfileSerializer


class LeaderBoardView(APIView):
    def get(self, request):
        profile = PayableProfile.objects.all()
        serializer = PayableProfileSerializer(profile, many=True)
        return Response(serializer.data)
