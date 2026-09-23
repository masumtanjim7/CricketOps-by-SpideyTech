import uuid
from django.db import models
from django.conf import settings

class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='player_profile'
    )
    public_id = models.CharField(max_length=20, unique=True)
    verification_status = models.CharField(max_length=50, default='unverified')

    def __str__(self):
        return self.public_id