from rest_framework import serializers
from .models import *
import decimal
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.utils import translation
from django.utils.translation import override as translation_override

from rest_framework import serializers
from django.utils.translation import gettext as _
from order.models import Order, TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['id', 'phone', 'chat_id']

    def get_queryset(self):
        return TelegramUser.objects.all().order_by('id')

class OrderSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSummary
        fields = ['chat_id', 'orders']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Ensure Decimal values are serialized properly
        representation['orders'] = self._convert_decimals(representation['orders'])
        
        # Create a mapping of existing orders by order_id
        existing_orders = {order['order_id']: order for order in representation['orders']}
        
        # Incoming orders from validated data
        incoming_orders = self.initial_data.get('orders', [])
        
        # Process incoming orders
        for new_order in incoming_orders:
            order_id = new_order.get('order_id')
            if order_id in existing_orders:
                # Update the existing order's fields
                existing_orders[order_id].update(new_order)
            else:
                # Add new order if it does not exist
                existing_orders[order_id] = new_order
        
        # Convert the dictionary back to a list for output
        updated_orders = list(existing_orders.values())
        
        # Filter to include only necessary fields: 'submitted_at' and 'latest_status_time'
        filtered_orders = []
        for order in updated_orders:
            # Determine latest status and corresponding timestamp
            latest_status_time = None
            latest_status = None
            
            # Check each possible status and its timestamp
            for status in ['submitted', 'created', 'processed', 'complete', 'canceled']:
                status_time = order.get(f"{status}_at")  # Assumes you have timestamp fields like submitted_at, created_at, etc.
                
                if status_time is not None:
                    if latest_status_time is None or status_time > latest_status_time:
                        latest_status_time = status_time
                        latest_status = status
            
            filtered_order = {
                'order_id': order['order_id'],
                'submitted_at': order.get('submitted_at'),  # Make sure this field exists in your order data
                'latest_status_time': latest_status_time,
                'latest_status': latest_status  # The status name (like 'processed', etc.)
            }
            filtered_orders.append(filtered_order)

        representation['orders'] = filtered_orders
        return representation

    def _convert_decimals(self, data):
        if isinstance(data, dict):
            return {key: self._convert_decimals(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._convert_decimals(item) for item in data]
        elif isinstance(data, decimal.Decimal):
            return float(data)
        return data

    def validate_chat_id(self, value):
        if not value:
            raise serializers.ValidationError("chat_id cannot be null.")
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False, write_only=True)
    product_id = serializers.CharField(write_only=True)  # Accept product_id in the request
    total_sum = serializers.DecimalField(max_digits=10, decimal_places=2)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    color_value = serializers.CharField(source='product.color_value', read_only=True)
    size = serializers.CharField(source='product.size', read_only=True)

    # English fields
    color_name_en = serializers.CharField(source='product.color_name_en', read_only=True)
    name_en = serializers.CharField(source='product.name_en', read_only=True)
    collection_name_en = serializers.CharField(source='product.collection.name_en', read_only=True)

    # Ukrainian fields
    color_name_uk = serializers.CharField(source='product.color_name_uk', read_only=True)
    name_uk = serializers.CharField(source='product.name_uk', read_only=True)
    collection_name_uk = serializers.CharField(source='product.collection.name_uk', read_only=True)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def validate(self, data):
        product_id = data.get('product_id')
        if not product_id:
            raise serializers.ValidationError({'product': 'This field is required.'})

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product': 'Product does not exist.'})
        data['product'] = product
        return data

    class Meta:
        model = OrderItem
        fields = [
            'product_id', 'product', 'quantity', 'total_sum', 'price', 'color_value', 'size',
            'name_en', 'color_name_en', 'collection_name_en',
            'name_uk', 'color_name_uk', 'collection_name_uk'
        ]

class OrderSerializer(serializers.ModelSerializer):
    order_items_en = serializers.SerializerMethodField()
    order_items_uk = serializers.SerializerMethodField()
    telegram_user = serializers.PrimaryKeyRelatedField(queryset=TelegramUser.objects.all(), required=False)

    class Meta:
        model = Order
        fields = [
            'id', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments',
            'congrats', 'submitted_at', 'created_at', 'processed_at', 'complete_at', 'canceled_at',
            'parent_order', 'present', 'status', 'order_items_en', 'order_items_uk', 'telegram_user'
        ]

    def get_order_items_en(self, obj):
        return self._get_order_items(obj, language='en')

    def get_order_items_uk(self, obj):
        return self._get_order_items(obj, language='uk')

    def _get_order_items(self, obj, language=None):
        items = []
        for item in obj.order_items.all():
            product = item.product

            # Fetch English translation values or default to '_('No Name')'
            name_en = product.name_en if product.name_en else _('No Name')
            color_name_en = product.color_name_en if product.color_name_en else _('No Color')
            collection_name_en = product.collection.name_en if product.collection and product.collection.name_en else _('No Collection')

            # Fetch Ukrainian translation values or default to '_('No Name')'
            name_uk = product.name_uk if product.name_uk else _('No Name')
            color_name_uk = product.color_name_uk if product.color_name_uk else _('No Color')
            collection_name_uk = product.collection.name_uk if product.collection and product.collection.name_uk else _('No Collection')

            # Add the order items for both languages
            if language == 'en':
                items.append({
                    'size': product.size,
                    'quantity': item.quantity,
                    'color_name': color_name_en,
                    'price': str(product.price),
                    'color_value': product.color_value,
                    'name': name_en,
                    'collection_name': collection_name_en,
                })
            elif language == 'uk':
                items.append({
                    'size': product.size,
                    'quantity': item.quantity,
                    'color_name': color_name_uk,
                    'price': str(product.price),
                    'color_value': product.color_value,
                    'name': name_uk,
                    'collection_name': collection_name_uk,
                })

        return items