from django.urls import path
import playable.views as view

urlpatterns = [
    path('add_tournament/', view.add_tournament, name='add_tournament'),
    path('edit_tournament/<str:ext_id>/', view.edit_tournament, name='edit_tournament'),
    path('list_tournament/', view.list_tournament, name='list_tournament'),
]
