import uuid
from django.db import models
from organizations.models import Organization

class Tournament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='tournaments')
    format = models.CharField(max_length=50) # e.g., T20, ODI
    status = models.CharField(max_length=50, default='scheduled')

    def __str__(self):
        return str(self.id)