from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.contrib import admin
from django.urls import path, include

from user import views
from user.serializer import MyTokenObtainPairView


urlpatterns = [
    path('oj/admin/', admin.site.urls),

    path('oj/portal/', views.login_admin, name='admin_login'),
    path('oj/portal/admin_logout/', views.logout_admin, name='admin_logout'),
    path('oj/portal/workflow/', views.show_workflow, name='workflow'),
    path('oj/portal/user/', include('user.portal_urls')),
    path('oj/portal/team/', include('team.portal_urls')),
    path('oj/portal/playable/', include('playable.portal_urls')),
    path('oj/portal/office/', include('office.portal_urls')),

    path('oj/api/user/', include('user.api_urls')),
    path('oj/api/playable/', include('playable.api_urls')),
    path('oj/api/payable/', include('payable.api_urls')),
    path('oj/api/office/', include('office.api_urls')),

    path('oj/api/auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('oj/api/auth/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('oj/api/auth/token-verify/', TokenVerifyView.as_view(), name='token_verify'),
]
