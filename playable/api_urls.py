from django.urls import path
from playable.views import UpcommingView, MatchView, YourBetsView

urlpatterns = [
    path('upcomming/', UpcommingView.as_view()),
    path('match/<str:ext_id>', MatchView.as_view()),
    path('your-bets/', YourBetsView.as_view())
]
