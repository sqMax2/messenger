from django.contrib import admin
from django.contrib.admin import ModelAdmin

from msngr.models import Room, Member


class RoomAdmin(ModelAdmin):
    list_display = ['name', 'get_online_count']


class MemberAdmin(ModelAdmin):
    list_display = [field.name for field in Member._meta.get_fields()]


admin.site.register(Room, RoomAdmin)
admin.site.register(Member, MemberAdmin)
