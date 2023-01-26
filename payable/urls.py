from django.urls import path
from payable.views import CoinsView, BetView, BetList

urlpatterns = [
    path('coins/<str:ext_id>', CoinsView.as_view()),
    path('bet/', BetList.as_view()),
    path('bet/<str:ext_id>', BetView.as_view()),
]
