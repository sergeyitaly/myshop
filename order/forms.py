from django import forms
from django.core.exceptions import ValidationError
from shop.models import Product  # Import your Product model here

class OrderForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    address = forms.CharField(label='Shipping Address', widget=forms.Textarea)
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'type': 'tel'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise ValidationError("Phone number is required.")
        if len(phone) < 10:
            raise ValidationError("Phone number must be at least 10 digits long.")
        return phone

class OrderItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Product')
    quantity = forms.IntegerField(label='Quantity', min_value=1)

OrderItemFormSet = forms.formset_factory(OrderItemForm, extra=1)
