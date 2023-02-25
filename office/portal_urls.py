from django.urls import path
import office.views as views

urlpatterns = [

    path('add_task/', views.add_task, name='add_task'),
    path('list_task/', views.list_task, name='list_task'),
    path('edit_task/<str:ext_id>/', views.edit_task, name='edit_task'),
]
