from django.urls import path
import office.views as views
from office.views import LeaderBoardView, TaskView

urlpatterns = [
    path('leaderboard/', LeaderBoardView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('add_task/', views.add_task, name='add_task'),
    path('list_task/', views.list_task, name='list_task'),
    path('edit_task/<str:ext_id>/', views.edit_task, name='edit_task'),
]
