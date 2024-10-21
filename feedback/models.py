from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

# 1. Model for questions and rating names (aspects)
class RatingQuestion(models.Model):
    question = models.CharField(max_length=255, default='Question is ...',verbose_name="Rating Question")
    aspect_name = models.CharField(max_length=255, verbose_name="Aspect Name")

    def __str__(self):
        return self.aspect_name


# 2. Model for feedback (answers and rating values)
class Feedback(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Feedback contains multiple ratings related to RatingQuestion
    ratings = models.ManyToManyField(
        RatingQuestion,
        through='RatingAnswer',
        related_name='feedbacks'
    )

    STATUS_CHOICES = [
        ('processed', 'Processed'),
        ('complete', 'Complete'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processed')

    def __str__(self):
        return f"Feedback from {self.name}"
    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

# Model to link Feedback and RatingQuestion with the rating value
class RatingAnswer(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    question = models.ForeignKey(RatingQuestion, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Rating"
    )

    def __str__(self):
        return f"{self.question.aspect_name}: {self.rating}"

# 3. Model for overall average calculations
class OverallAverageRating(models.Model):
    question = models.OneToOneField(
        RatingQuestion,
        on_delete=models.CASCADE,
        related_name='average_rating'
    )
    average_rating = models.FloatField(default=0, editable=False)

    def __str__(self):
        return f"Average for {self.question.aspect_name}: {self.average_rating}"

    @classmethod
    def calculate_overall_averages(cls):
        """Calculate average ratings for all RatingQuestions."""
        for question in RatingQuestion.objects.all():
            avg_rating = RatingAnswer.objects.filter(question=question).aggregate(average=Avg('rating'))['average'] or 0
            overall_avg, created = cls.objects.get_or_create(question=question)
            overall_avg.average_rating = avg_rating
            overall_avg.save()
