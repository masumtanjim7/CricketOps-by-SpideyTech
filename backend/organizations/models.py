import uuid
from django.db import models
from django.conf import settings

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    verification_status = models.CharField(max_length=50, default='pending')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='owned_organizations'
    )

    def __str__(self):
        return self.name