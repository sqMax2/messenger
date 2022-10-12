"""
msngr app views
"""
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions, authentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
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


# REST custom permissions
class ObjectPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.user.is_authenticated:
            match view.basename:
                case 'member':
                    view.queryset = view.queryset.filter(user__username=request.user.username)
                case 'user':
                    view.queryset = view.queryset.filter(username=request.user.username)
                case 'room':
                    return True
                case _:
                    return False
            try:
                # disallowing change of other user's data
                view.response
                if view.response.status_code == 404:
                    return False
            except:
                pass
            if request.method != 'POST':
                # only staff users and django can do POST request
                return True
            else:
                return False

            # if request.method == 'GET':
            #
            #     print(view.queryset)
            #     return True
            # else:
            #     return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            # staff users can do everything
            return True
        if request.user.is_authenticated:
            match view.basename:
                case 'member':
                    username = obj.user.username
                case 'user':
                    username = obj.username
                case 'room':
                    # in rooms every authenticated user can do everything
                    return True
                case _:
                    return False
            if username == request.user.username:
                return True
            else:
                return False
        else:
            return False


class RoomViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ObjectPermission]
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
    lookup_field = 'user'
    lookup_fields = ['user', 'pk']

    permission_classes = [permissions.IsAuthenticated, ObjectPermission]
    queryset = Member.objects.all()
    serializer_class = MemberSerializer




    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        print(self.kwargs)
        for field in self.lookup_fields:
            if self.kwargs.get(field, None):
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


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
    permission_classes = [permissions.IsAuthenticated, ObjectPermission]
