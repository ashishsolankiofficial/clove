from django.urls import path
import user.views as view

urlpatterns = [

    path('admin_registration/', view.admin_registration, name='admin_registration'),
    path('admin_edit/<str:ext_id>/', view.admin_registration, name='admin_edit'),
    path('admin_list/', view.admin_list, name='admin_list'),
    path('user_registration/', view.user_registration, name='user_registration'),
    path('user_edit/<str:ext_id>/', view.admin_registration, name='user_edit'),
    path('user_list/', view.user_list, name='user_list'),
]
