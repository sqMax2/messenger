"""
authapp urls config
"""

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from .views import BaseRegisterView, ProfileView

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('profile/',
         ProfileView.as_view(template_name='sign/profile.html'),
         name='profile'),
]
