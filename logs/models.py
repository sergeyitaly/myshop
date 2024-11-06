# models.py
from django.db import models

class APILog(models.Model):
    endpoint = models.CharField(max_length=255)
    has_chat_id = models.BooleanField(default=False)
    request_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.endpoint} - {self.request_count}"
