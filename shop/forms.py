from django import forms
from django_svg_image_form_field import SvgAndImageFormField
from .models import Product, Collection, ProductImage


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
            'brandimage': SvgAndImageFormField,

        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['images']
