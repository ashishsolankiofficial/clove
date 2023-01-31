from django.urls import path
from office.views import LeaderBoardView

urlpatterns = [
    path('leaderboard/', LeaderBoardView.as_view())
]
