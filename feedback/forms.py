from django import forms
from .models import Feedback, RatingAnswer, RatingQuestion


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.questions = RatingQuestion.objects.all()
        for question in self.questions:
            self.fields[f'question_{question.id}_rating'] = forms.IntegerField(
                label=question.aspect_name,
                min_value=1,
                max_value=10,
                required=question.rating_required,
                widget=forms.NumberInput(attrs={'class': 'rating-input'}),
            )
            self.fields[f'question_{question.id}_answer'] = forms.CharField(
                label=f"Answer for {question.question}",
                required=False,
                widget=forms.Textarea(attrs={'class': 'answer-input', 'rows': 2}),
            )

    def clean(self):
        cleaned_data = super().clean()
        for question in self.questions:
            if question.rating_required:
                rating_value = cleaned_data.get(f'question_{question.id}_rating')
                if rating_value is None:
                    self.add_error(f'question_{question.id}_rating', "This field is required.")
        return cleaned_data

    def save(self, commit=True):
        feedback = super().save(commit=commit)
        rating_answers = []
        for question in self.questions:
            rating_value = self.cleaned_data.get(f'question_{question.id}_rating')
            answer_value = self.cleaned_data.get(f'question_{question.id}_answer')
            if rating_value is not None:
                rating_answers.append(
                    RatingAnswer(feedback=feedback, question=question, rating=rating_value, answer=answer_value)
                )
        if rating_answers:
            RatingAnswer.objects.bulk_create(rating_answers)
        return feedback
