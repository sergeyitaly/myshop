from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.db import transaction
from .models import RatingAnswer, OverallAverageRating, RatingQuestion

def update_average_for_question(question):
    """Helper function to update or delete the average rating for a given question."""
    if not question.rating_required:
        # Delete OverallAverageRating if the question does not require ratings
        OverallAverageRating.objects.filter(question=question).delete()
        return None

    # Calculate the average rating
    avg_rating = RatingAnswer.objects.filter(question=question).aggregate(average=Avg('rating'))['average'] or 0
    avg_rating = round(avg_rating, 1)

    # Get or create the OverallAverageRating object and update the average rating
    overall_avg, created = OverallAverageRating.objects.get_or_create(question=question)
    overall_avg.average_rating = avg_rating
    overall_avg.save()
    return overall_avg


@receiver(post_save, sender=RatingAnswer)
@receiver(post_delete, sender=RatingAnswer)
def update_average_rating(sender, instance, **kwargs):
    """Update the average rating for all questions whenever a RatingAnswer is saved or deleted."""
    with transaction.atomic():  # Ensure atomic updates
        overall_avgs = []
        for question in RatingQuestion.objects.all():
            overall_avg = update_average_for_question(question)
            if overall_avg:
                overall_avgs.append(overall_avg)

        # Bulk update to improve efficiency
        OverallAverageRating.objects.bulk_update(overall_avgs, ['average_rating'])


@receiver(post_delete, sender=RatingQuestion)
def delete_overall_average_ratings(sender, instance, **kwargs):
    """Delete OverallAverageRating when a RatingQuestion is deleted."""
    OverallAverageRating.objects.filter(question=instance).delete()
