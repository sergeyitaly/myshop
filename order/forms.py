from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import xml.etree.cElementTree as et
from django_svg_image_form_field import SvgAndImageFormField
from shop.models import Product  # Import your Product model here


class OrderForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    address = forms.CharField(label='Shipping Address', widget=forms.Textarea)

class OrderItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(label='Quantity', min_value=1)

OrderItemFormSet = forms.formset_factory(OrderItemForm, extra=1)