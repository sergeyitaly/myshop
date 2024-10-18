from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RatingAnswer, OverallAverageRating
from django.db.models import Avg

@receiver(post_save, sender=RatingAnswer)
def update_average_rating(sender, instance, **kwargs):
    """
    Signal that calculates and updates the average rating for each question
    whenever a RatingAnswer is saved or updated.
    """
    question = instance.question
    
    # Calculate the average rating for this particular question
    avg_rating = RatingAnswer.objects.filter(question=question).aggregate(average=Avg('rating'))['average'] or 0
    
    # Update or create the OverallAverageRating entry for this question
    overall_avg, created = OverallAverageRating.objects.get_or_create(question=question)
    overall_avg.average_rating = avg_rating
    overall_avg.save()
