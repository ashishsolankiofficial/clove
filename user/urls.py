from django.urls import path
import user.views as view

urlpatterns = [
    path('registration/', view.user_registration)
]
