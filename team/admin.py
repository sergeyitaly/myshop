from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import TeamMember
from .translator import * 
from django.utils.translation import gettext_lazy as _  
from django.utils.html import format_html
from django.contrib import admin

@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin):
    list_display = ('id', 'image_tag','name_en', 'name_uk', 'surname_en', 'surname_uk', 'mobile', 'email',)
    search_fields = ('name_en', 'name_uk', 'surname_en', 'surname_uk', 'mobile', 'linkedin')
    readonly_fields = ('id', 'image_tag')

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format(obj.photo_thumbnail.url))
        else:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format('collection.jpg'))
    image_tag.short_description = _("Image")