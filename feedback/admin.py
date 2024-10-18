from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Feedback, OverallAverageRating, RatingQuestion, RatingAnswer
from modeltranslation.admin import TranslationAdmin
from .translator import * 

@admin.register(RatingQuestion)
class RatingQuestionAdmin(TranslationAdmin):
    list_display = ['question_en', 'question_uk','aspect_name_uk','aspect_name_en']
    search_fields = ['question_en', 'question_uk','aspect_name_uk','aspect_name_en']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment', 'status', 'created_at']
    list_filter = ['status']
    readonly_fields = ['name', 'email', 'comment']

    def save_model(self, request, obj, form, change):
        """Override to recalculate the overall average rating after saving a feedback."""
        super().save_model(request, obj, form, change)
        self.update_overall_average_ratings()

    def update_overall_average_ratings(self):
        """Calculate the overall average ratings and update the OverallAverageRating model."""
        OverallAverageRating.calculate_overall_averages()

@admin.register(RatingAnswer)
class RatingAnswerAdmin(admin.ModelAdmin):
    list_display = ['feedback', 'question', 'rating', 'answer']
    list_filter = ['question']
    search_fields = ['feedback__name', 'question__aspect_name']
    raw_id_fields = ['feedback', 'question']  # Use raw_id fields for better performance with large datasets

@admin.register(OverallAverageRating)
class OverallAverageRatingAdmin(admin.ModelAdmin):
    list_display = ['question', 'average_rating']
    readonly_fields = ['average_rating']

    def has_add_permission(self, request):
        """Prevent creating new OverallAverageRating instances through the admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the OverallAverageRating instance."""
        return False

    def average_rating(self, obj):
        """Display the average rating."""
        return obj.average_rating

    average_rating.short_description = _("Average Rating")

def register_translation_admin(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except admin.sites.NotRegistered:
        admin.site.register(model, admin.ModelAdmin)
    