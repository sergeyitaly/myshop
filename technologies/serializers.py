from rest_framework import serializers
from .models import Technology

class TechnologySerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Technology
        fields = ['name', 'name_en', 'name_uk', 'description', 'description_en', 'description_uk','link', 'photo_url', 'photo_thumbnail_url']

    def get_photo_url(self, obj):
        if obj.photo and hasattr(obj.photo, 'url'):
            return obj.photo.url
        return None

    def get_photo_thumbnail_url(self, obj):
        if obj.photo_thumbnail and hasattr(obj.photo_thumbnail, 'url'):
            return obj.photo_thumbnail.url
        return None