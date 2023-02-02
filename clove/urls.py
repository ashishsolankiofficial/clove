from django.contrib import admin
from django.urls import path, include
from user import views
from user.serializer import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_admin, name='admin_login'),
    path('admin_logout/', views.logout_admin, name='admin_logout'),
    path('workflow/', views.show_workflow, name='workflow'),

    path('user/', include('user.urls')),
    path('team/', include('team.urls')),
    path('playable/', include('playable.urls')),
    path('payable/', include('payable.urls')),
    path('office/', include('office.urls')),

    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token-verify/', TokenVerifyView.as_view(), name='token_verify'),
]
