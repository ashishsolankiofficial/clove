from django.urls import path
import team.views as view

urlpatterns = [
    path('add_team/', view.add_team, name='add_team'),
    path('list_team/', view.list_team, name='list_team')
]
