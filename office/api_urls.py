from django.urls import path
from office.views import LeaderBoardView, TaskView

urlpatterns = [
    path('leaderboard/', LeaderBoardView.as_view()),
    path('tasks/', TaskView.as_view()),
]
