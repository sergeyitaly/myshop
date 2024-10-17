from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields =['name', 'email', 'comment',
             'question1', 'answer1', 'rating_1', 
             'question2', 'answer2', 'rating_2',
             'question3', 'answer3', 'rating_3', 
             'question4', 'answer4', 'rating_4',
             'question5', 'answer5', 'rating_5', 
             'question6', 'answer6', 'rating_6',
             'question7', 'answer7', 'rating_7', 
             'question8', 'answer8', 'rating_8',
             'question9', 'answer9', 'rating_9', 
             'question10', 'answer10', 'rating_10']

        widgets = {
            'rating_1': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'rating_2': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'rating_3': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'rating_4': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'rating_5': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'rating_6': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'rating_7': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'rating_8': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'rating_9': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'rating_10': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
