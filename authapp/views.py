from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView

from msngr.models import Member
from .models import BaseRegisterForm, ProfileForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Member
    form_class = ProfileForm
    template_name = 'sign/profile.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user.member

    def get_initial(self):
        initial = super(ProfileView, self).get_initial()
        initial['username'] = self.request.user.username
        return initial

    # def get_context_data(self, **kwargs):
    #     form = self.form_class(self.request.GET)
    #     form.fields['username'].initial = self.request.user.username
    #     print(form.fields['username'].__dict__)
    #     return super(ProfileView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        return super(ProfileView, self).form_valid(form)
    
    def post(self, request, *args, **kwargs):
        user = self.get_object().user
        user.username = request._post['username']
        user.save()
        return super().post(request, *args, **kwargs)
