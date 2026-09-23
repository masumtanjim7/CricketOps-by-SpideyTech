import uuid
from django.db import models
from matches.models import Innings
from players.models import Player

class BatterInnings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    innings = models.ForeignKey(Innings, on_delete=models.CASCADE, related_name='batter_projections')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batting_innings')
    runs = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='yet_to_bat') # e.g., batting, out, retired
    strike_rate = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('innings', 'player')

class BowlerInnings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    innings = models.ForeignKey(Innings, on_delete=models.CASCADE, related_name='bowler_projections')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowling_innings')
    balls_bowled = models.IntegerField(default=0)
    runs_conceded = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    maidens = models.IntegerField(default=0)
    economy = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('innings', 'player')

class CareerAggregate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='career_stats')
    format = models.CharField(max_length=50) # e.g., T20, ODI
    matches_played = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    total_wickets = models.IntegerField(default=0)
    recalculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('player', 'format')