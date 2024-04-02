from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm 
from django.forms import EmailInput, ModelForm, PasswordInput
from .models import CustomUser 
 
class CustomUserCreationForm(UserCreationForm):   
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=PasswordInput)
    email = forms.CharField(widget=EmailInput) 
    class Meta:        
        model = CustomUser        
        fields = ('email', 'username', )  
        
class CustomUserChangeForm(UserChangeForm):    
    class Meta:        
        model = CustomUser        
        fields = UserChangeForm.Meta.fields