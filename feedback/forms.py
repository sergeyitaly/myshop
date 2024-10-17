from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email','comment', 'rating_1', 'rating_2', 'rating_3', 'rating_4', 'rating_5', 'rating_6', 'rating_7', 'rating_8', 'rating_9', 'rating_10']
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
