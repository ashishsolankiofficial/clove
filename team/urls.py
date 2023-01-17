from django.urls import path
import team.views as view

urlpatterns = [
    path('add_team/', view.add_team, name='add_team'),
    path('edit_team/<str:ext_id>', view.edit_team, name='edit_team'),
    path('list_team/', view.list_team, name='list_team')
]
