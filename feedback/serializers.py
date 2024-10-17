from rest_framework import serializers
from .models import Feedback, OverallAverageRating

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            'name', 'email','comment',
            'question1', 'answer1', 
            'question2', 'answer2',
            'question3', 'answer3', 
            'question4', 'answer4',
            'question5', 'answer5', 
            'question6', 'answer6',
            'question7', 'answer7', 
            'question8', 'answer8',
            'question9', 'answer9', 
            'question10', 'answer10',
            'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5',
            'rating_6', 'rating_7', 'rating_8', 'rating_9', 'rating_10',
             'status', 'created_at'
        ]


class OverallAverageRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallAverageRating
        fields = [
            'avg_rating_1', 'avg_rating_2', 'avg_rating_3', 'avg_rating_4', 'avg_rating_5',
            'avg_rating_6', 'avg_rating_7', 'avg_rating_8', 'avg_rating_9', 'avg_rating_10'
        ]
