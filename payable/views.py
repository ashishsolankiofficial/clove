from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from playable.models import BilateralMatch
from office.models import Office
from user.models import User
from payable.models import PayableProfile, BilateralBet, UnsettledBet
from payable.serializer import CoinSerializer, BetSerializer, UnsettledBetSerializer

# Create your views here.


class CoinsView(APIView):
    def get(self, request, ext_id):
        payable_profile = PayableProfile.objects.get(user__ext_id=ext_id)
        serializer = CoinSerializer(payable_profile)
        return Response(serializer.data)


class BetList(APIView, PageNumberPagination):
    page_size = 20

    def get(self, request, format=None):
        query_set = UnsettledBet.objects.filter(user__ext_id=request.user.ext_id)
        query_set = self.paginate_queryset(query_set, request, view=self)
        serializer = UnsettledBetSerializer(query_set, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        request.data['office'] = User.objects.get(ext_id=request.user.ext_id).office.ext_id
        serializer = BetSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BetView(APIView):

    def get(self, request, ext_id):
        bilateral_bet = BilateralBet.objects.get(ext_id=ext_id)
        serializer = BetSerializer(bilateral_bet)
        return Response(serializer.data)

    def put(self, request, ext_id, format=None):
        bilateral_bet = get_object_or_404(BilateralBet, ext_id=ext_id)
        request.data['office'] = User.objects.get(ext_id=request.user.ext_id).office.ext_id
        serializer = BetSerializer(bilateral_bet, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
