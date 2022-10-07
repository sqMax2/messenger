"""
msngr app views
"""
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

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
    lookup_field = 'name'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(methods=['patch'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def join(self, request, *args, **kwargs):
        room_obj = self.get_object()
        room_obj.join(request.user)
        return JsonResponse({'result': 'success'})

    @action(methods=['patch'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def leave(self, request, *args, **kwargs):
        room_obj = self.get_object()
        room_obj.leave(request.user)
        return JsonResponse({'result': 'success'})


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
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
