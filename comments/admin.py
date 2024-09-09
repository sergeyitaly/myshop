from django.contrib import admin
from .models import Comment
from .translator import * 
from django.utils.translation import gettext_lazy as _  
from modeltranslation.admin import TranslationAdmin

@admin.register(Comment)
class CommentAdmin(TranslationAdmin):
    list_display = ['name', 'email', 'phone_number', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email', 'phone_number', 'comment']

# Helper function to register translated models
def register_translation_admin(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except admin.sites.NotRegistered:
        admin.site.register(model, admin.ModelAdmin)
    