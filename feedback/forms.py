from django import forms
from .models import Feedback, RatingAnswer, RatingQuestion


class FeedbackForm(forms.ModelForm):
    """
    Form for collecting feedback details and dynamically adding rating fields based on RatingQuestion.
    """
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'comment']  # Feedback basic fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically add rating fields for each RatingQuestion
        questions = RatingQuestion.objects.all()

        for question in questions:
            self.fields[f'question_{question.id}_rating'] = forms.IntegerField(
                label=question.aspect_name,
                min_value=1,
                max_value=10,
                required=True,
                widget=forms.NumberInput(attrs={'class': 'rating-input'}),
            )
            self.fields[f'question_{question.id}_answer'] = forms.CharField(
                label=f"Answer for {question.question}",
                required=False,
                widget=forms.Textarea(attrs={'class': 'answer-input', 'rows': 2}),
            )

    def save(self, commit=True):
        # Save the Feedback instance first
        feedback = super().save(commit=commit)

        # Save the associated RatingAnswers
        questions = RatingQuestion.objects.all()

        for question in questions:
            rating_value = self.cleaned_data.get(f'question_{question.id}_rating')
            answer_value = self.cleaned_data.get(f'question_{question.id}_answer')

            if rating_value:
                # Create or update the RatingAnswer for this question and feedback
                RatingAnswer.objects.update_or_create(
                    feedback=feedback,
                    question=question,
                    defaults={'rating': rating_value, 'answer': answer_value},
                )

        return feedback
