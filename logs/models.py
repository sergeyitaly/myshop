from django.db import models

class APILog(models.Model):
    endpoint = models.CharField(max_length=255)
    has_chat_id = models.BooleanField(default=False)
    request_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)  # Use auto_now for updates

    class Meta:
        unique_together = ('endpoint', 'has_chat_id')  # Ensure uniqueness for endpoint and chat_id combo
        ordering = ['-timestamp']  # Default ordering by most recent

    def __str__(self):
        return f"Endpoint: {self.endpoint}, Chat ID: {self.has_chat_id}, Requests: {self.request_count}"
