from rest_framework import serializers
from .models import TeamMember

class TeamMemberSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = ['name', 'name_en', 'name_uk', 'surname', 'surname_en', 'surname_uk', 'mobile', 'linkedin', 'photo_url', 'photo_thumbnail_url']

    def get_photo_url(self, obj):
        if obj.photo and hasattr(obj.photo, 'url'):
            return obj.photo.url
        return None

    def get_photo_thumbnail_url(self, obj):
        if obj.photo_thumbnail and hasattr(obj.photo_thumbnail, 'url'):
            return obj.photo_thumbnail.url
        return None
