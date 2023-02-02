from django.urls import path
import user.views as view
from user.views import UserProfileView

urlpatterns = [

    path('add_admin/', view.add_admin, name='add_admin'),
    path('edit_admin/<str:ext_id>/', view.edit_admin, name='edit_admin'),
    path('list_admin/', view.list_admin, name='list_admin'),
    path('add_user/', view.add_user, name='add_user'),
    path('edit_user/<str:ext_id>/', view.edit_user, name='edit_user'),
    path('list_user/', view.list_user, name='list_user'),

    path('profile/<str:ext_id>/', UserProfileView.as_view())
]
