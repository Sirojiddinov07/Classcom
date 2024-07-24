import uuid

from django.db import models
from django.utils import timezone


class DownloadToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    download = models.ForeignKey("Download", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at
