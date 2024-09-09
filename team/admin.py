from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import TeamMember
from .translator import * 
from django.utils.translation import gettext_lazy as _  
from django.utils.html import format_html


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
    list_display = ('id','name_en', 'name_uk', 'name_en', 'surname_uk','mobile', 'linkedin')
    search_fields = ('name_en', 'name_uk', 'name_en', 'surname_uk','mobile', 'linkedin')
    readonly_fields = ('id', 'image_tag')

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format(obj.photo_thumbnail.url))
        else:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format('collection.jpg'))
    image_tag.short_description = _("Image")

# Helper function to register translated models
def register_translation_admin(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except admin.sites.NotRegistered:
        admin.site.register(model, admin.ModelAdmin)
