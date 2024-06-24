from django.utils import timezone

from django.db import models

from core.http.models import User


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    massage = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    response = models.TextField(null=True, blank=True)
    response_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Chat by {self.user} to admin "

    def save(self, *args, **kwargs):
        if self.response:
            self.response_time = timezone.now()
        super().save(*args, **kwargs)