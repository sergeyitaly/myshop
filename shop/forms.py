# forms.py
from django import forms
from .models import Product, Collection, ProductImage, AdditionalField
from django_svg_image_form_field import SvgAndImageFormField

class AdditionalFieldForm(forms.ModelForm):
    class Meta:
        model = AdditionalField
        fields = '__all__' 


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = '__all__' 


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__' 

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__' 
