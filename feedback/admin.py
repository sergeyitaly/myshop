from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Feedback, OverallAverageRating, RatingQuestion, RatingAnswer
from modeltranslation.admin import TranslationAdmin
from .translator import RatingQuestion
from django.utils import formats
from django.http import HttpResponseRedirect
from django.urls import reverse
from adminsortable2.admin import SortableAdminMixin


class RatingAnswerInline(admin.TabularInline):
    model = RatingAnswer
    extra = 0  # Number of empty forms to display
    readonly_fields = ['answer', 'rating'] 

    def has_change_permission(self, request, obj=None):
        return False 

    def has_add_permission(self, request, obj=None):
        return False    
    def has_delete_permission(self, request, obj=None):
        return False  # Disable delete permission

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(self, 'parent_object') and self.parent_object:
            return qs.filter(question=self.parent_object)
        return qs

@admin.register(RatingQuestion)
class RatingQuestionAdmin(SortableAdminMixin, TranslationAdmin):
    list_display = ['id', 'question_en', 'question_uk', 'order']
    search_fields = ['question_en', 'question_uk', 'aspect_name_uk', 'aspect_name_en']
    inlines = [RatingAnswerInline]  # Inline answers displayed in the RatingQuestion admin

    def delete_model(self, request, obj):
        OverallAverageRating.objects.filter(question=obj).delete()
        super().delete_model(request, obj)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'comment', 'status', 'formatted_created_at']
    list_filter = ['status']  # Filter by feedback status
    search_fields = ['name', 'email', 'comment']  # Add search capability
    readonly_fields = ['name', 'email', 'comment']  # Make these fields read-only
    inlines = [RatingAnswerInline]  # Include RatingAnswer inline editing

    def has_delete_permission(self, request, obj=None):
        return True  # Disable delete permission

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.update_overall_average_ratings()

    def update_overall_average_ratings(self):
        OverallAverageRating.calculate_overall_averages()

    def has_add_permission(self, request):
        return False

    def formatted_created_at(self, obj):
        return formats.date_format(obj.created_at, use_l10n=True)
    formatted_created_at.admin_order_field = 'created_at'
    formatted_created_at.short_description = _("Created At")

@admin.register(OverallAverageRating)
class OverallAverageRatingAdmin(SortableAdminMixin,admin.ModelAdmin):
    list_display = ['question', 'average_rating', 'order'] 
    readonly_fields = ['question','average_rating']  
    search_fields = ['question__question_en', 'question__question_uk'] 

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    

    def update_overall_average_ratings(self):
        OverallAverageRating.calculate_overall_averages()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        self.update_overall_average_ratings()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(question__rating_required=True).select_related('question') 

    def change_view(self, request, object_id, form_url='', extra_context=None):
        overall_avg_rating = self.get_object(request, object_id)
        if overall_avg_rating and overall_avg_rating.question:
            # Redirect to the RatingQuestion change page
            rating_question_id = overall_avg_rating.question.id
            return HttpResponseRedirect(reverse('admin:feedback_ratingquestion_change', args=[rating_question_id]))       
        return super().change_view(request, object_id, form_url, extra_context)    

def register_translation_admin(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except admin.sites.NotRegistered:
        admin.site.register(model, admin.ModelAdmin)