from rest_framework import serializers
from .models import Brand

class BrandSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)

    class Meta:
        model = Brand
        fields = ['name', 'name_en', 'name_uk', 'linke', 'photo', 'photo_thumbnail']
