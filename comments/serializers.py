from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'phone_number', 'comment', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']
