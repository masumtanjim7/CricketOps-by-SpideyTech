from django.contrib import admin
from .models import ScoringSession, Delivery, Wicket, MatchSnapshot, Correction

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'innings', 'sequence', 'striker', 'bowler', 'bat_runs', 'extras_total', 'legal_delivery')
    list_filter = ('legal_delivery',)

@admin.register(MatchSnapshot)
class MatchSnapshotAdmin(admin.ModelAdmin):
    list_display = ('match', 'score', 'overs', 'version', 'updated_at')