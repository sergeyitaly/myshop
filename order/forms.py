from django import forms
from django.core.exceptions import ValidationError
from shop.models import Product  # Import your Product model here
from django.utils.translation import gettext_lazy as _

class OrderForm(forms.Form):

    DELIVERY_CHOICES = ( 
        ('self_pickup', _('Self Pickup')), 
        ('nova_poshta', _('Nova Poshta')), 
        ('ukr_poshta', _('Ukr Poshta')), ) 
    PAYMENT_CHOICES = ( 
        ('cash_on_delivery', _('Cash on Delivery')), 
        ('card_online', _('Online Card Payment')), )  
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    address = forms.CharField(label='Shipping Address', widget=forms.Textarea)
    phone = forms.CharField(label='Phone', widget=forms.TextInput(attrs={'type': 'tel'}))
    receiver = forms.CharField(label='Receiver')
    receiver_comments = forms.CharField(label='Receiver_Coments')
    congrats = forms.CharField(label='Congrats')
    delivery = forms.CharField(label=('Delivery Method')) 
    payment = forms.CharField(labele=('Payment Method'))



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
