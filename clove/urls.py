from django.contrib import admin
from django.urls import path, include
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_admin, name='admin_login'),
    path('admin_logout/', views.logout_admin, name='admin_logout'),
    path('workflow/', views.show_workflow, name='workflow'),
    path('user/', include('user.urls')),
    path('team/', include('team.urls')),
    path('playable/', include('playable.urls')),
]
