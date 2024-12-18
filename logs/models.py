from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Count

class APILog(models.Model):
    endpoint = models.URLField()
    request_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        app_label = 'logs'  

    def __str__(self):
        return f"Endpoint: {self.endpoint}, Requests: {self.request_count}"

    @classmethod
    def update_request_count(cls, endpoint):
        count = cls.objects.filter(endpoint=endpoint).count()
        cls.objects.filter(endpoint=endpoint).update(request_count=count)

@receiver(post_save, sender=APILog)
def recalculate_request_count_on_create(sender, instance, created, **kwargs):
    if created:
        APILog.update_request_count(instance.endpoint)

@receiver(post_delete, sender=APILog)
def recalculate_request_count_on_delete(sender, instance, **kwargs):
    APILog.update_request_count(instance.endpoint)

class IgnoreEndpoint(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        app_label = 'logs'

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"IgnoreEndpoint: {self.name} ({status})"