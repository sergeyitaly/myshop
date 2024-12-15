from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

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

@receiver(post_delete, sender=APILog)
def recalculate_request_count(sender, instance, **kwargs):
    endpoint = instance.endpoint
    request_count = APILog.objects.filter(endpoint=endpoint).count()
    APILog.objects.filter(endpoint=endpoint).update(request_count=request_count)