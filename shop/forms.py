from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import xml.etree.cElementTree as et
from django_svg_image_form_field import SvgAndImageFormField
from .models import Product, Collection, Category


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        exclude = []
        field_classes = {
            'photo': SvgAndImageFormField,
        }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []
        field_classes = {
            'photo': SvgAndImageFormField,
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
