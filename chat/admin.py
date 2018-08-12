from django.contrib import admin
from .models import RoomChat


class AdminRoomChat(admin.ModelAdmin):
    list_display = ['name', 'time_created', 'created_by']
    search_fields = ['name']
    list_filter = ['name']
    list_per_page = 5


admin.site.register(RoomChat, AdminRoomChat)