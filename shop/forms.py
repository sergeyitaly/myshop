# forms.py
from django import forms
from .models import Product, Collection, ProductImage, AdditionalField
from django_svg_image_form_field import SvgAndImageFormField

class AdditionalFieldForm(forms.ModelForm):
    custom_name = forms.CharField(label='Field Name')
    custom_value = forms.CharField(label='Field Value', widget=forms.Textarea)

    class Meta:
        model = AdditionalField
        fields = ['custom_name', 'custom_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['custom_name'].initial = self.instance.name
            self.fields['custom_value'].initial = self.instance.value

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data['custom_name']
        instance.value = self.cleaned_data['custom_value']
        if commit:
            instance.save()
        return instance

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
