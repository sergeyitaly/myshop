from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class APILog(models.Model):
    endpoint = models.URLField()
    request_count = models.IntegerField(default=1)  # Always 1 for each request
    timestamp = models.DateTimeField(auto_now=True)
    request_sum = models.IntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']
        app_label = 'logs'

    def __str__(self):
        return f"Endpoint: {self.endpoint}, Requests: {self.request_count}"

    @classmethod
    def update_request_sum(cls, endpoint):
        # Efficient aggregation using `annotate`
        total_requests = cls.objects.filter(endpoint=endpoint).count()
        cls.objects.filter(endpoint=endpoint).update(request_sum=total_requests)


class IgnoreEndpoint(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        app_label = 'logs'

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"IgnoreEndpoint: {self.name} ({status})"
