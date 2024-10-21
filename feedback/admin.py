from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Feedback, OverallAverageRating, RatingQuestion, RatingAnswer
from modeltranslation.admin import TranslationAdmin
from .translator import RatingQuestion

@admin.register(RatingQuestion)
class RatingQuestionAdmin(TranslationAdmin):
    list_display = ['question_en', 'question_uk','aspect_name_uk','aspect_name_en']
    search_fields = ['question_en', 'question_uk','aspect_name_uk','aspect_name_en']

class RatingAnswerInline(admin.TabularInline):
    model = RatingAnswer
    extra = 0  # Number of empty forms to display

    # Ensure the question field is a dropdown of RatingQuestion instances
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = RatingQuestion.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment', 'status', 'created_at']
    list_filter = ['status']
 #   readonly_fields = ['name', 'email', 'comment']
    inlines = [RatingAnswerInline]
    
    def save_model(self, request, obj, form, change):
        """Override to recalculate the overall average rating after saving a feedback."""
        super().save_model(request, obj, form, change)
        self.update_overall_average_ratings()

    def update_overall_average_ratings(self):
        """Calculate the overall average ratings and update the OverallAverageRating model."""
        OverallAverageRating.calculate_overall_averages()
    
@admin.register(OverallAverageRating)
class OverallAverageRatingAdmin(admin.ModelAdmin):
    list_display = ['question', 'average_rating']  # Display the question and the calculated average rating
    readonly_fields = ['average_rating']  # Make the average_rating field read-only

    def has_add_permission(self, request):
        """Prevent creating new OverallAverageRating instances through the admin."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the OverallAverageRating instance."""
        return False
    def update_overall_average_ratings(self):
        """Calculate the overall average ratings and update the OverallAverageRating model."""
        OverallAverageRating.calculate_overall_averages()
    def save_model(self, request, obj, form, change):
        """Override to recalculate the overall average rating after saving a feedback."""
        super().save_model(request, obj, form, change)
        self.update_overall_average_ratings()

def register_translation_admin(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except admin.sites.NotRegistered:
        admin.site.register(model, admin.ModelAdmin)
    