from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe

from msngr.models import Room, Member


class RoomAdmin(ModelAdmin):
    list_display = ['name', 'get_online_count']


class MemberAdmin(ModelAdmin):
    list_display = [field.name for field in Member._meta.get_fields()]
    readonly_fields = ['avatar_img']

    def avatar_img(self, obj):
        return mark_safe('<img src="{url}" style="max-width:{width}; max-height:{height};" />'.format(
            url=obj.avatar.url,
            width='200px',
            height='200px',))


admin.site.register(Room, RoomAdmin)
admin.site.register(Member, MemberAdmin)
