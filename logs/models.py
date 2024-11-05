from django.db import models

class APILog(models.Model):
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    chat_id = models.BigIntegerField()
    command = models.CharField(max_length=100)
    source = models.CharField(max_length=20, choices=[('Telegram Bot', 'Telegram Bot'), ('Vercel', 'Vercel')], default='Vercel')
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.command} - {self.timestamp}"