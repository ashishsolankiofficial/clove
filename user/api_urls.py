from django.urls import path
from user.views import UserProfileView, ResetPassword

urlpatterns = [

    path('reset-password/', ResetPassword.as_view()),
    path('profile/<str:ext_id>/', UserProfileView.as_view())
]
