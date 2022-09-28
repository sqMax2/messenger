"""
msngr app views
"""
from django.contrib.auth.models import User
from django.shortcuts import render


def index(request):
    return render(request, 'msngr/index.html')


def room(request, room_name):
    return render(request, 'msngr/room.html', {
        'room_name': room_name,
        'username': request.user.username,
    })
