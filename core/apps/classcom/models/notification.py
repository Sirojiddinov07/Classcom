from django.db import models

from core.http.models.base import AbstractBaseModel
from core.http.models.user import User


class Notification(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='notifications')
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.phone} | {self.message}"
    
    class Meta:
        db_table = 'notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        