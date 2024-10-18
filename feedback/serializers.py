from rest_framework import serializers
from .models import RatingQuestion, Feedback, RatingAnswer, OverallAverageRating


# Serializer for RatingQuestion
class RatingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingQuestion
        fields = ['id', 'question','aspect_name']


# Serializer for RatingAnswer
class RatingAnswerSerializer(serializers.ModelSerializer):
    question = RatingQuestionSerializer(read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(queryset=RatingQuestion.objects.all(), write_only=True, source='question')

    class Meta:
        model = RatingAnswer
        fields = ['id', 'question', 'question_id', 'answer', 'rating']


# Serializer for Feedback
class FeedbackSerializer(serializers.ModelSerializer):
    ratings = RatingAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'name', 'comment', 'email', 'created_at', 'status', 'ratings']

    def create(self, validated_data):
        # Handle nested RatingAnswer creation
        ratings_data = validated_data.pop('ratings')
        feedback = Feedback.objects.create(**validated_data)

        for rating_data in ratings_data:
            RatingAnswer.objects.create(feedback=feedback, **rating_data)

        return feedback

    def update(self, instance, validated_data):
        ratings_data = validated_data.pop('ratings', None)
        instance.name = validated_data.get('name', instance.name)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.email = validated_data.get('email', instance.email)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if ratings_data:
            for rating_data in ratings_data:
                question_id = rating_data.get('question_id')
                rating_answer = RatingAnswer.objects.filter(feedback=instance, question=question_id).first()
                if rating_answer:
                    rating_answer.rating = rating_data.get('rating', rating_answer.rating)
                    rating_answer.answer = rating_data.get('answer', rating_answer.answer)
                    rating_answer.save()
                else:
                    RatingAnswer.objects.create(feedback=instance, **rating_data)

        return instance


# Serializer for OverallAverageRating
class OverallAverageRatingSerializer(serializers.ModelSerializer):
    model = OverallAverageRating
    question = RatingQuestionSerializer(read_only=True)

    class Meta:
        model = OverallAverageRating
        fields = ['question', 'average_rating']
