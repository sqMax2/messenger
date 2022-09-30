"""
msngr app views
"""
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import GroupChat, Member
from .serializers import GroupChatSerializer, MemberSerializer, UserSerializer


def index(request):
    return render(request, 'msngr/index.html')


def room(request, room_name):
    return render(request, 'msngr/room.html', {
        'room_name': room_name,
        'username': request.user.username,
    })


class GroupChatViewset(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer


class MemberViewset(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
