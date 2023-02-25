from django.contrib import admin
from django.urls import path, include
from user import views
from user.serializer import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', views.login_admin, name='admin_login'),
    path('portal/admin_logout/', views.logout_admin, name='admin_logout'),
    path('portal/workflow/', views.show_workflow, name='workflow'),

    path('api/user/', include('user.api_urls')),
    path('portal/user/', include('user.portal_urls')),
    path('portal/team/', include('team.portal_urls')),
    path('portal/playable/', include('playable.portal_urls')),
    path('api/playable/', include('playable.api_urls')),
    path('api/payable/', include('payable.api_urls')),
    path('portal/office/', include('office.portal_urls')),
    path('api/office/', include('office.api_urls')),

    path('api/auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token-verify/', TokenVerifyView.as_view(), name='token_verify'),
]
