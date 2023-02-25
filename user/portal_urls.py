from django.urls import path
import user.views as views

urlpatterns = [

    path('add_admin/', views.add_admin, name='add_admin'),
    path('edit_admin/<str:ext_id>/', views.edit_admin, name='edit_admin'),
    path('list_admin/', views.list_admin, name='list_admin'),
    path('list_inactive_admin/', views.list_inactive_admin, name='list_inactive_admin'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<str:ext_id>/', views.edit_user, name='edit_user'),
    path('list_user/', views.list_user, name='list_user'),
    path('list_inactive_user/', views.list_inactive_user, name='list_inactive_user'),

]
