from django.contrib import admin
from .models import Match, MatchTeam, PlayingXI, Innings

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'version', 'scheduled_at')

@admin.register(Innings)
class InningsAdmin(admin.ModelAdmin):
    list_display = ('match', 'batting_team', 'number', 'version', 'status')