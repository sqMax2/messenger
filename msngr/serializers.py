"""
msngr REST serializers
"""
from django.contrib.admin.utils import lookup_field

from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')

    class Meta:
        model = User
        fields = ['id', 'username', 'url', 'email', 'first_name', 'last_name', 'is_staff', 'last_login', 'date_joined',
                  'member']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    online = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        # read_only=True,
        many=True,
        slug_field='username'
    )
    # online = UserSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='room-detail', lookup_field='name')

    class Meta:
        model = Room
        fields = ['name', 'online', 'get_online_count', 'url']
        extra_kwargs = {'url': {'lookup_field': 'name'}}


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='member-detail', lookup_field='pk')
    # user_url = serializers.HyperlinkedRelatedField(view_name='user-detail', lookup_field='username',
    #                                            queryset=User.objects.all())
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Member
        fields = ['user', 'avatar', 'url']
