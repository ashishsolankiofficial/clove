from django.urls import path
import playable.views as view
from playable.views import UpcommingView, MatchView, YourBetsView

urlpatterns = [
    path('add_tournament/', view.add_tournament, name='add_tournament'),
    path('edit_tournament/<str:ext_id>/', view.edit_tournament, name='edit_tournament'),
    path('list_tournament/', view.list_tournament, name='list_tournament'),
    path('list_inactive_tournament/', view.list_inactive_tournament, name='list_inactive_tournament'),
    path('add_match/<str:t_id>', view.add_match, name='add_match'),
    path('edit_match/<str:t_id>/<str:ext_id>/', view.edit_match, name='edit_match'),
    path('list_match/<str:t_id>/', view.list_match, name='list_match'),
    path('list_inactive_match/<str:t_id>/', view.list_inactive_match, name='list_inactive_match'),
    path('choose_winner/<str:t_id>/<str:ext_id>/', view.choose_winner, name='choose_winner'),
    path('distribute_rewards/<str:t_id>/<str:ext_id>/', view.distribute_rewards, name='distribute_rewards'),

    path('upcomming/', UpcommingView.as_view()),
    path('match/<str:ext_id>', MatchView.as_view()),
    path('your-bets/', YourBetsView.as_view())
]
