from rest_framework import serializers
from .models import TeamMember

class TeamMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)
    surname = serializers.CharField()
    surname_en = serializers.CharField(required=False)
    surname_uk = serializers.CharField(required=False)
    
    class Meta:
        model = TeamMember
        fields = ['name', 'name_en', 'name_uk', 'surname', 'surname_en','surname_uk','mobile', 'linkedin', 'photo', 'photo_thumbnail']
