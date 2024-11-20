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
        elif isinstance(data, datetime.datetime):
            return data.isoformat()  # Convert datetime to ISO format
        return data


    def validate_chat_id(self, value):
        if not value:
            raise serializers.ValidationError("chat_id cannot be null.")
        return value

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False, write_only=True)
#    product_id = serializers.CharField(write_only=True)  # Accept product_id in the request
    product_id = serializers.IntegerField(write_only=True)

    total_sum = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
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
    
    def get_total_sum(self, obj):
        return obj.total_sum 
    
    class Meta:
        model = OrderItem
        fields = [
            'product_id', 'product', 'quantity', 'total_sum', 'price', 'color_value', 'size',
            'name_en', 'color_name_en', 'collection_name_en',
            'name_uk', 'color_name_uk', 'collection_name_uk'
        ]




class OrderSerializer(serializers.ModelSerializer):
    order_items_en = OrderItemSerializer(many=True, read_only=True)
    order_items_uk = OrderItemSerializer(many=True, read_only=True)
    telegram_user = serializers.PrimaryKeyRelatedField(queryset=TelegramUser.objects.all(), required=False)

    class Meta:
        model = Order
        fields = [
            'id', 'language', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments',
            'congrats', 'submitted_at', 'created_at', 'processed_at', 'complete_at', 'canceled_at',
            'parent_order', 'present', 'status', 'order_items_en', 'order_items_uk', 'telegram_user'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        order_items_en, order_items_uk = self.get_order_items(instance)
        representation['order_items_en'] = order_items_en
        representation['order_items_uk'] = order_items_uk
        return representation



    def get_order_items(self, obj):
        # Return the order items in both languages
        return self._get_order_items(obj)

    def _get_order_items(self, obj):
        items_en = []
        items_uk = []
        for item in obj.order_items.all():
            product = item.product

            # Define default values
            default_name = _("No Name")
            default_color = _("No Color")
            default_collection = _("No Collection")

            item_data_en = {
                'size': product.size,
                'quantity': item.quantity,
                'price': product.price,
                'color_value': product.color_value,
                'name': product.name_en or default_name,
                'color_name': product.color_name_en or default_color,
                'collection_name': (product.collection.name_en if product.collection else None) or default_collection,
            }

            item_data_uk = {
                'size': product.size,
                'quantity': item.quantity,
                'price': product.price,
                'color_value': product.color_value,
                'name': product.name_uk or default_name,
                'color_name': product.color_name_uk or default_color,
                'collection_name': (product.collection.name_uk if product.collection else None) or default_collection,
            }

            items_en.append(item_data_en)
            items_uk.append(item_data_uk)

        return items_en, items_uk
