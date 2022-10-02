"""
msngr REST serializers
"""

from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login', 'date_joined',
                  'member']


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    online = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        # read_only=True,
        many=True,
        slug_field='username'
    )
    # online = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['name', 'online', 'get_online_count']
        # depth = 1


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=User.objects.all())
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Member
        fields = ['user', 'avatar']


# class RoomUserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Member
