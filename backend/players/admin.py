from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('public_id', 'user', 'verification_status')
    search_fields = ('public_id',)