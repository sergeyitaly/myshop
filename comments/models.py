from django.db import models
from django.utils.translation import gettext_lazy as _

class Comment(models.Model):
    STATUS_CHOICES = [
        ('processed', 'Processed'),
        ('complete', 'Complete'),
    ]

    name = models.CharField(max_length=255,verbose_name=_('Name'))
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    comment = models.TextField(verbose_name=_('Comment'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.status}'
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
