"""
msngr app views
"""
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Room, Member
from .serializers import RoomSerializer, MemberSerializer, UserSerializer
from channels.layers import get_channel_layer


def index(request):
    return render(request, 'msngr/index.html')


def room(request, room_name):
    return render(request, 'msngr/room.html', {
        'room_name': room_name,
        'username': request.user.username,
    })


class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MemberViewset(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


# class RoomMemberViewset(viewsets.ModelViewSet):
#     queryset = Member.objects.all()
#     serializer_class = MemberSerializer
#
#     def get_queryset(self):
#         room_name = self.kwargs['room_name']
#         channel_layer = get_channel_layer()
#         return Member.objects.all()


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
