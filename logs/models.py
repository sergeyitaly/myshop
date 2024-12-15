from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class APILog(models.Model):
    endpoint = models.CharField(max_length=255)
    has_chat_id = models.BooleanField(default=False)
    request_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)  # Use auto_now for updates

    class Meta:
        unique_together = ('endpoint', 'has_chat_id')  # Ensure uniqueness for endpoint and chat_id combo
        ordering = ['-timestamp']  # Default ordering by most recent
        app_label = 'logs'  
        
    def __str__(self):
        return f"Endpoint: {self.endpoint}, Chat ID: {self.has_chat_id}, Requests: {self.request_count}"

    @classmethod
    def update_request_count(cls, endpoint):
        """Update request count for all logs with the given endpoint."""
        count = cls.objects.filter(endpoint=endpoint).count()
        cls.objects.filter(endpoint=endpoint).update(request_count=count)

@receiver(post_save, sender=APILog)
def recalculate_request_count_on_create(sender, instance, created, **kwargs):
    """Recalculate the request count when a new APILog is created."""
    if created:
        APILog.update_request_count(instance.endpoint)

@receiver(post_delete, sender=APILog)
def recalculate_request_count_on_delete(sender, instance, **kwargs):
    """Recalculate the request count when an APILog entry is deleted."""
    APILog.update_request_count(instance.endpoint)
