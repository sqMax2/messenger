from django.contrib import admin
from django.contrib.admin import ModelAdmin

from msngr.models import GroupChat, Member


class GroupChatAdmin(ModelAdmin):
    list_display = ['name', ]


class MemberAdmin(ModelAdmin):
    list_display = ['user', 'avatar', ]


admin.site.register(GroupChat, GroupChatAdmin)
admin.site.register(Member, MemberAdmin)
