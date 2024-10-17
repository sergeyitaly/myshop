from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Feedback(models.Model):
    # String fields for feedback details
    name = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Integer fields for star ratings (1 to 10)
    rating_1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 1", blank=True)
    question1 = models.TextField(verbose_name="Question 1", null=True, blank=True)
    answer1 = models.TextField(verbose_name="Answer 1",null=True, blank=True)

    rating_2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 2", blank=True)
    question2 = models.TextField(verbose_name="Question 2", null=True, blank=True)
    answer2 = models.TextField(verbose_name="Answer 2",null=True, blank=True )

    rating_3 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 3", blank=True)
    question3 = models.TextField(verbose_name="Question 3", null=True, blank=True)
    answer3 = models.TextField(verbose_name="Answer 2",null=True, blank=True )

    rating_4 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 4", blank=True)
    question4 = models.TextField(verbose_name="Question 4", null=True, blank=True)
    answer4 = models.TextField(verbose_name="Answer 4",null=True, blank=True )

    rating_5 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 5", blank=True)
    question5 = models.TextField(verbose_name="Question 5", null=True, blank=True)
    answer5 = models.TextField(verbose_name="Answer 5",null=True, blank=True )

    rating_6 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 6", blank=True)
    question6 = models.TextField(verbose_name="Question 6", null=True, blank=True)
    answer6 = models.TextField(verbose_name="Answer 6",null=True, blank=True )

    rating_7 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 7", blank=True)
    question7 = models.TextField(verbose_name="Question 7", null=True, blank=True)
    answer7 = models.TextField(verbose_name="Answer 7",null=True, blank=True )

    rating_8 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 8", blank=True)
    question8 = models.TextField(verbose_name="Question 8", null=True, blank=True)
    answer8 = models.TextField(verbose_name="Answer 8",null=True, blank=True )

    rating_9 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 9", blank=True)
    question9 = models.TextField(verbose_name="Question 9", null=True, blank=True)
    answer9 = models.TextField(verbose_name="Answer 9",null=True, blank=True )

    rating_10 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Rating for aspect 10", blank=True)
    question10 = models.TextField(verbose_name="Question 10", null=True, blank=True)
    answer10 = models.TextField(verbose_name="Answer 10",null=True, blank=True )
 
    STATUS_CHOICES = [
        ('processed', 'Processed'),
        ('complete', 'Complete'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processed')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback from {self.name}"

class OverallAverageRating(models.Model):
    """Stores the overall average ratings across all feedback entries."""
    avg_rating_1 = models.FloatField(default=0, editable=False)
    avg_rating_2 = models.FloatField(default=0, editable=False)
    avg_rating_3 = models.FloatField(default=0, editable=False)
    avg_rating_4 = models.FloatField(default=0, editable=False)
    avg_rating_5 = models.FloatField(default=0, editable=False)
    avg_rating_6 = models.FloatField(default=0, editable=False)
    avg_rating_7 = models.FloatField(default=0, editable=False)
    avg_rating_8 = models.FloatField(default=0, editable=False)
    avg_rating_9 = models.FloatField(default=0, editable=False)
    avg_rating_10 = models.FloatField(default=0, editable=False)

    def __str__(self):
        return "Overall Average Ratings"

    @classmethod
    def calculate_overall_averages(cls):
        """Calculate the overall average of all feedback ratings and update the OverallAverageRating model."""
        feedbacks = Feedback.objects.all()
        avg_rating_1 = feedbacks.aggregate(Avg('rating_1'))['rating_1__avg'] or 0
        avg_rating_2 = feedbacks.aggregate(Avg('rating_2'))['rating_2__avg'] or 0
        avg_rating_3 = feedbacks.aggregate(Avg('rating_3'))['rating_3__avg'] or 0
        avg_rating_4 = feedbacks.aggregate(Avg('rating_4'))['rating_4__avg'] or 0
        avg_rating_5 = feedbacks.aggregate(Avg('rating_5'))['rating_5__avg'] or 0
        avg_rating_6 = feedbacks.aggregate(Avg('rating_6'))['rating_6__avg'] or 0
        avg_rating_7 = feedbacks.aggregate(Avg('rating_7'))['rating_7__avg'] or 0
        avg_rating_8 = feedbacks.aggregate(Avg('rating_8'))['rating_8__avg'] or 0
        avg_rating_9 = feedbacks.aggregate(Avg('rating_9'))['rating_9__avg'] or 0
        avg_rating_10 = feedbacks.aggregate(Avg('rating_10'))['rating_10__avg'] or 0

        # Update the OverallAverageRating instance (assuming there's only one record)
        overall_avg, created = cls.objects.get_or_create(id=1)
        overall_avg.avg_rating_1 = avg_rating_1
        overall_avg.avg_rating_2 = avg_rating_2
        overall_avg.avg_rating_3 = avg_rating_3
        overall_avg.avg_rating_4 = avg_rating_4
        overall_avg.avg_rating_5 = avg_rating_5
        overall_avg.avg_rating_6 = avg_rating_6
        overall_avg.avg_rating_7 = avg_rating_7
        overall_avg.avg_rating_8 = avg_rating_8
        overall_avg.avg_rating_9 = avg_rating_9
        overall_avg.avg_rating_10 = avg_rating_10
        overall_avg.save()