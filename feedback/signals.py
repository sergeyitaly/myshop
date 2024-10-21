from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.db import transaction
from .models import RatingAnswer, OverallAverageRating, RatingQuestion

def update_average_for_question(question):
    """Helper function to update average rating for a given question."""
    avg_rating = RatingAnswer.objects.filter(question=question).aggregate(average=Avg('rating'))['average'] or 0
    overall_avg, created = OverallAverageRating.objects.get_or_create(question=question)
    overall_avg.average_rating = avg_rating
    return overall_avg

@receiver(post_save, sender=RatingAnswer)
def update_average_rating(sender, instance, **kwargs):
    """Update the average rating for all questions whenever a RatingAnswer is saved or updated."""
    with transaction.atomic():  # Ensure all updates are done atomically
        overall_avgs = []  # List to hold updated OverallAverageRating instances
        for question in RatingQuestion.objects.all():
            overall_avg = update_average_for_question(question)
            overall_avgs.append(overall_avg)  # Append to the updates list

        OverallAverageRating.objects.bulk_update(overall_avgs, ['average_rating'])  # Efficiently update all at once

@receiver(post_delete, sender=RatingAnswer)
def update_average_rating_on_delete(sender, instance, **kwargs):
    """Update the average rating for all questions whenever a RatingAnswer is deleted."""
    with transaction.atomic():  # Ensure all updates are done atomically
        overall_avgs = []  # List to hold updated OverallAverageRating instances
        for question in RatingQuestion.objects.all():
            overall_avg = update_average_for_question(question)
            overall_avgs.append(overall_avg)  # Append to the updates list

        OverallAverageRating.objects.bulk_update(overall_avgs, ['average_rating'])  # Efficiently update all at once
