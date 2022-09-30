"""
msngr REST serializers
"""

from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class GroupChatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupChat
        fields = ['name']


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=User.objects.all())
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Member
        fields = ['user', 'avatar']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login', 'date_joined', 'member']
