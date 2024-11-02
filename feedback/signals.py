from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.db import transaction
from .models import RatingAnswer, OverallAverageRating, RatingQuestion, Feedback

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

@receiver(post_save, sender=Feedback)
def update_average_rating_after_feedback(sender, instance, created, **kwargs):
    """Update the average rating for all questions related to the feedback after a new Feedback is saved."""
    if created:  # Only update when a new Feedback instance is created
        with transaction.atomic():
            # Iterate over the ratings associated with the feedback
            for rating_answer in instance.ratings.all():
                question = rating_answer.question
                update_average_for_question(question)

@receiver(post_delete, sender=Feedback)
def recalculate_average_rating_on_feedback_delete(sender, instance, **kwargs):
    """Recalculate the average ratings for all questions related to the feedback when Feedback is deleted."""
    with transaction.atomic():
        # Iterate over the ratings associated with the feedback
        for rating_answer in instance.ratings.all():
            question = rating_answer.question
            update_average_for_question(question)

@receiver(post_delete, sender=RatingQuestion)
def delete_overall_average_ratings(sender, instance, **kwargs):
    """Delete OverallAverageRating when a RatingQuestion is deleted."""
    OverallAverageRating.objects.filter(question=instance).delete()
