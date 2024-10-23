from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _

# 1. Model for questions and rating names (aspects)
class RatingQuestion(models.Model):
    question = models.CharField(max_length=255, default='Question is ...',verbose_name=_('Rating Question'))
    aspect_name = models.CharField(max_length=255, verbose_name=_('Aspect Name'),null=True,blank=True)
    rating_required = models.BooleanField(default=True, verbose_name=_('Is Rating Required'))  # New field
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order'] 
    def __str__(self):
        return self.aspect_name if self.aspect_name else self.question 


# 2. Model for feedback (answers and rating values)
class Feedback(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Name'))
    comment = models.TextField(null=True, blank=True,verbose_name=_('Comment'))
    email = models.EmailField(null=True, blank=True,verbose_name=_('Email'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Created At'))

    # Feedback contains multiple ratings related to RatingQuestion
    ratings = models.ManyToManyField(
        RatingQuestion,
        through='RatingAnswer',
        related_name='feedbacks',
        verbose_name=_('Ratings')
    )

    STATUS_CHOICES = [
        ('processed', 'Processed'),
        ('complete', 'Complete'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processed',verbose_name=_('Status'))

    def __str__(self):
        return f"Feedback from {self.name}"
    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

# Model to link Feedback and RatingQuestion with the rating value
class RatingAnswer(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, verbose_name=_('Feedback'))
    question = models.ForeignKey(RatingQuestion, on_delete=models.CASCADE, verbose_name=_('Question'))
    answer = models.TextField(null=True, blank=True, verbose_name=_('Answer'))
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,  # Allow NULL values
        blank=True,  # Allow the field to be blank
        verbose_name=_('Rating')  # Set verbose name for the field
    )

    def __str__(self):
        return f"{self.question.aspect_name}: {self.rating}"
    
    def save(self, *args, **kwargs):
        # Only require a rating if the question requires it
        if self.question.rating_required and self.rating is None:
            raise ValueError("Rating is required for this question.")
        super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.question.rating_required and self.rating is None:
            raise ValueError("Rating is required for this question.")
        super().save(*args, **kwargs)


# 3. Model for overall average calculations
class OverallAverageRating(models.Model):
    question = models.OneToOneField(
        RatingQuestion,
        on_delete=models.SET_NULL,
        null=True,
        related_name='average_rating',
        verbose_name=_('Question')
    )
    average_rating = models.FloatField(default=0, editable=False, verbose_name=_('Average Rating'))
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order'] 
    def __str__(self):
        return f"Average for {self.question.aspect_name}: {self.average_rating}"

    @classmethod
    def calculate_overall_averages(cls):
        """Calculate average ratings for all RatingQuestions."""
        for question in RatingQuestion.objects.all():
            avg_rating = RatingAnswer.objects.filter(question=question).aggregate(average=Avg('rating'))['average'] or 0
            
            avg_rating = round(avg_rating, 1)
            
            overall_avg, created = cls.objects.get_or_create(question=question)
            overall_avg.average_rating = avg_rating
            overall_avg.save()
