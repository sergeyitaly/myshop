from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Feedback, OverallAverageRating, RatingQuestion, RatingAnswer
from modeltranslation.admin import TranslationAdmin
from .translator import RatingQuestion
from django.utils import formats

class RatingAnswerInline(admin.TabularInline):
    model = RatingAnswer
    extra = 0  # Number of empty forms to display
    readonly_fields = ['answer', 'rating'] 
    # Ensure the question field is a dropdown of RatingQuestion instances
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "question":
            kwargs["queryset"] = RatingQuestion.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        """Prevent editing of RatingAnswer instances."""
        return False 

    def has_add_permission(self, request, obj=None):
        """Prevent creating new OverallAverageRating instances through the admin."""
        return False    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of Feedback instances through the admin."""
        return False # Disable delete permission

@admin.register(RatingQuestion)
class RatingQuestionAdmin(TranslationAdmin):
    list_display = ['id','question_en', 'question_uk','aspect_name_uk','aspect_name_en']
    search_fields = ['question_en', 'question_uk','aspect_name_uk','aspect_name_en']
    inlines = [RatingAnswerInline]
    def delete_model(self, request, obj):
        OverallAverageRating.objects.filter(question=obj).delete()
        super().delete_model(request, obj)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # Display columns in the admin table
    list_display = ['id', 'name', 'email', 'comment', 'status', 'formatted_created_at']
    list_filter = ['status']  # Filter by feedback status
    search_fields = ['name', 'email', 'comment']  # Add search capability
    readonly_fields = ['name', 'email', 'comment']  # Make these fields read-only
    inlines = [RatingAnswerInline]  # Include RatingAnswer inline editing

    # Prevent feedback deletion
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of Feedback instances through the admin."""
        return True  # Disable delete permission

    def save_model(self, request, obj, form, change):
        """Override to recalculate the overall average rating after saving feedback."""
        super().save_model(request, obj, form, change)
        self.update_overall_average_ratings()

    def update_overall_average_ratings(self):
        """Calculate the overall average ratings and update the OverallAverageRating model."""
        OverallAverageRating.calculate_overall_averages()
    def has_add_permission(self, request):
        """Prevent creating new OverallAverageRating instances through the admin."""
        return False
    
    def formatted_created_at(self, obj):
        return formats.date_format(obj.created_at, use_l10n=True)    
    formatted_created_at.admin_order_field = 'created_at'  
    formatted_created_at.short_description = _("Created At")



@admin.register(OverallAverageRating)
class OverallAverageRatingAdmin(admin.ModelAdmin):
    list_display = ['question', 'average_rating'] 
    readonly_fields = ['average_rating']  
    list_filter = ['question'] 
    search_fields = ['question__question_en', 'question__question_uk'] 

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

    def get_queryset(self, request):
        """Customize the queryset to ensure it includes only required questions."""
        qs = super().get_queryset(request)
        # Filter to include only OverallAverageRating with questions requiring a rating
        return qs.filter(question__rating_required=True).select_related('question')  
    

def register_translation_admin(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except admin.sites.NotRegistered:
        admin.site.register(model, admin.ModelAdmin)
    