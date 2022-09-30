from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from msngr.models import Member
from .models import BaseRegisterForm, ProfileForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class ProfileView(CreateView):
    model = Member
    form_class = ProfileForm
