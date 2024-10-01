# forms.py
from django import forms
from .models import Product, Collection, ProductImage, AdditionalField
from django_svg_image_form_field import SvgAndImageFormField

class AdditionalFieldForm(forms.ModelForm):
    class Meta:
        model = AdditionalField
        exclude = []


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        exclude = []
        field_classes = {
            'photo': SvgAndImageFormField,  # Allow both SVG and regular image files
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []
        field_classes = {
            'photo': SvgAndImageFormField,  # Allow both SVG and regular image files
            'brandimage': SvgAndImageFormField,  # Allow both SVG and regular image files
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['images']
