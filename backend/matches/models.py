import uuid
from django.db import models
from tournaments.models import Tournament
from teams.models import Team
from players.models import Player

class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True, blank=True, related_name='matches')
    status = models.CharField(max_length=50, default='scheduled')
    version = models.IntegerField(default=1)
    scheduled_at = models.DateTimeField(null=True, blank=True)

class MatchTeam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match_teams')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    side = models.CharField(max_length=50) # e.g., team_a, team_b
    toss_choice = models.CharField(max_length=50, null=True, blank=True)

class PlayingXI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match_team = models.ForeignKey(MatchTeam, on_delete=models.CASCADE, related_name='playing_xi')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    is_captain = models.BooleanField(default=False)
    is_keeper = models.BooleanField(default=False)

class Innings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='innings')
    batting_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    number = models.IntegerField()
    target = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')
    version = models.IntegerField(default=1)