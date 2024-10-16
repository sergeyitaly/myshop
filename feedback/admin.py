from django.contrib import admin
from .models import Feedback, OverallAverageRating

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment', 'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5', 
                    'rating_6', 'rating_7', 'rating_8', 'rating_9', 'rating_10']
    readonly_fields = ['question1', 'answer1', 'question2', 'answer2']

@admin.register(OverallAverageRating)
class OverallAverageRatingAdmin(admin.ModelAdmin):
    list_display = [
        'avg_rating_1', 'avg_rating_2', 'avg_rating_3', 'avg_rating_4', 'avg_rating_5',
        'avg_rating_6', 'avg_rating_7', 'avg_rating_8', 'avg_rating_9', 'avg_rating_10'
    ]
    readonly_fields = [
        'avg_rating_1', 'avg_rating_2', 'avg_rating_3', 'avg_rating_4', 'avg_rating_5',
        'avg_rating_6', 'avg_rating_7', 'avg_rating_8', 'avg_rating_9', 'avg_rating_10'
    ]

    def has_add_permission(self, request):
        """Prevent creating new OverallAverageRating instances through the admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the OverallAverageRating instance."""
        return False
