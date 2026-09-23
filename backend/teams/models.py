import uuid
from django.db import models
from organizations.models import Organization
from players.models import Player

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='active')

    def __str__(self):
        return self.name

class TeamMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='teams')
    role = models.CharField(max_length=50) 
    start_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='active')

    def __str__(self):
        return f"{self.player.public_id} - {self.team.name}"