from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Feedback

@receiver(post_save, sender=Feedback)
def update_ratings_on_feedback_save(sender, instance, **kwargs):
    """Signal to update overall averages when feedback is saved."""
    instance.update_overall_average_ratings()
