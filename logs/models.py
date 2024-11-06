from django.db import models

class APILog(models.Model):
    endpoint = models.CharField(max_length=255)
    request_count = models.IntegerField(default=0)
    has_chat_id = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.endpoint
