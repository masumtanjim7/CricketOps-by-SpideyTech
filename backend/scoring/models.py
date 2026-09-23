import uuid
from django.db import models
from django.conf import settings
from matches.models import Match, Innings
from players.models import Player

class ScoringSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='scoring_session')
    scorer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    lease_status = models.CharField(max_length=50, default='active')

class Delivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    innings = models.ForeignKey(Innings, on_delete=models.CASCADE, related_name='deliveries')
    sequence = models.IntegerField()
    striker = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='deliveries_faced')
    non_striker = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='deliveries_non_striker')
    bowler = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='deliveries_bowled')
    bat_runs = models.IntegerField(default=0)
    extras_total = models.IntegerField(default=0)
    legal_delivery = models.BooleanField(default=True)
    client_event_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

class DeliveryExtra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='extras')
    type = models.CharField(max_length=50) 
    amount = models.IntegerField(default=1)

class Wicket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='wicket')
    player_out = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='dismissals')
    kind = models.CharField(max_length=50)
    fielder = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='catches_runouts')
    bowler_credit = models.BooleanField(default=True)

class Correction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='corrections_original')
    replacement_delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='corrections_replacement', null=True, blank=True)
    reason = models.TextField()
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

class MatchSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='snapshot')
    score = models.IntegerField(default=0)
    overs = models.FloatField(default=0.0)
    target = models.IntegerField(null=True, blank=True)
    version = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)