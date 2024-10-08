from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Technology
from .translator import * 
from django.utils.translation import gettext_lazy as _  
from django.utils.html import format_html
from django.contrib import admin

@admin.register(Technology)
class IntroAdmin(TranslationAdmin):
    list_display = ('id', 'name_en', 'name_uk', 'link')
    search_fields = ('name_en', 'name_uk', 'link')
    readonly_fields = ('id', 'image_tag')

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format(obj.photo_thumbnail.url))
        else:
            return format_html('<img src="{}" style="max-height:150px; max-width:150px;" />'.format('collection.jpg'))
    image_tag.short_description = _("Image")