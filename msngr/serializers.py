"""
msngr REST serializers
"""
from django.contrib.admin.utils import lookup_field
from rest_framework.reverse import reverse

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

    # Example of custom method serialization
    # param = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['name', 'online', 'get_online_count', 'url']
        extra_kwargs = {'url': {'lookup_field': 'name'}}

    # Custom method
    # def get_param(self, obj):
    #     # return self.context['request'].GET.get('u','')
    #     # return print(self.context['request'].user)
    #     print(self)
    #     if self.context['request'].method == 'GET':
    #         return {'method': 'GET', 'params': self.context['request'].query_params}
    #     return self.context['request'].query_params


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='member-detail', lookup_field='pk')
    user_url = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    # user = UserSerializer()
    pk = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all())

    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Member
        fields = ['pk', 'user', 'user_url', 'avatar', 'url']

    def get_user_url(self, obj):
        result = '{}'.format(reverse('user-detail', args=[obj.user.username], request=self.context['request']))
        return result

