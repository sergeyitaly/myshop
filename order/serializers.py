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
import logging
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

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
        representation['orders'] = self._convert_decimals(representation['orders'])
        existing_orders = {order['order_id']: order for order in representation['orders']}
        incoming_orders = self.initial_data.get('orders', [])
        for new_order in incoming_orders:
            order_id = new_order.get('order_id')
            if order_id in existing_orders:
                existing_orders[order_id].update(new_order)
            else:
                existing_orders[order_id] = new_order
        
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
    product_id = serializers.IntegerField(write_only=True, required=False)
    total_sum = serializers.SerializerMethodField()

    # Other fields related to the product
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=1, read_only=True)
    currency = serializers.CharField(source='product.currency', read_only=True)

    color_value = serializers.CharField(source='product.color_value', read_only=True)
    size = serializers.CharField(source='product.size', read_only=True, required=False)

    # English fields
    color_name_en = serializers.CharField(source='product.color_name_en', read_only=True, required=False)
    name_en = serializers.CharField(source='product.name_en', read_only=True)
    collection_name_en = serializers.CharField(source='product.collection.name_en', read_only=True, required=False)

    # Ukrainian fields
    color_name_uk = serializers.CharField(source='product.color_name_uk', read_only=True, required=False)
    name_uk = serializers.CharField(source='product.name_uk', read_only=True)
    collection_name_uk = serializers.CharField(source='product.collection.name_uk', read_only=True, required=False)

    class Meta:
        model = OrderItem
        fields = [
            'product_id', 'quantity', 'price', 'currency','color_value', 'size', 'total_sum',
            'name_en', 'color_name_en', 'collection_name_en', 'name_uk', 'color_name_uk', 'collection_name_uk'
        ]

    def get_total_sum(self, obj):
        return obj.total_sum  # Return total_sum directly

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        return OrderItem.objects.create(product_id=product_id, **validated_data)
    

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)  # Keep order_items for creation
    order_items_en = serializers.SerializerMethodField()
    order_items_uk = serializers.SerializerMethodField()
    telegram_user = serializers.PrimaryKeyRelatedField(queryset=TelegramUser.objects.all(), required=False)

    def get_order_items_en(self, order):
        order_items = []
        for item in order.order_items.all():
            product = item.product
            collection = product.collection

            order_items.append({
                'product': {
                    'photo': product.photo.url if product.photo else None,  # Include photo if available
                    'name_en': product.name_en,  # Product name in English
                    'collection': {
                        'name_en': collection.name_en if collection else None  # Collection name in English
                    },
                    'price': product.price,  # Assuming `item` has a price field
                    'currency': product.currency,
                    'size': product.size,  # Item size
                    'color_name_en': product.color_name_en,  # Color name in English
                    'color_value': product.color_value,  # Color value (hex)
                },
                'quantity': item.quantity,  # Quantity of the item
                'total_sum': item.total_sum  # Total sum for the item
            })
        return order_items

    def get_order_items_uk(self, order):
        order_items = []
        for item in order.order_items.all():
            # Ensure product information is included
            product = item.product
            collection = product.collection  # Assuming the product has a related collection

            order_items.append({
                'product': {
                    'photo': product.photo.url if product.photo else None, 
                    'name_uk': product.name_uk,
                    'collection': {
                        'name_uk': collection.name_uk if collection else None 
                    },
                    'price': product.price,
                    'currency': product.currency,
                    'size': product.size,
                    'color_name_uk': product.color_name_uk,
                    'color_value': product.color_value,
                },
                'quantity': item.quantity,
                'total_sum': item.total_sum
            })
        return order_items


    def create(self, validated_data):
        items_data = validated_data.pop('order_items', [])
        telegram_user_data = validated_data.pop('telegram_user', None)

        telegram_user = None
        if telegram_user_data:
            telegram_user, created = TelegramUser.objects.get_or_create(
                phone=telegram_user_data.get('phone'),
                defaults={'chat_id': telegram_user_data.get('chat_id')}
            )
        order = Order.objects.create(telegram_user=telegram_user, **validated_data)
        for item_data in items_data:
            product_id = item_data.pop('product_id', None)
            if not product_id:
                raise ValidationError("product_id is required for order items.")
            
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise ValidationError(f"Product with id {product_id} does not exist.")

            order_item = OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'])
            print(f"Created OrderItem with product_id: {product_id}, OrderItem: {order_item}")

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items', [])
        telegram_user_data = validated_data.pop('telegram_user', None)
        language = validated_data.pop('language', instance.language)

        if telegram_user_data:
            telegram_user, created = TelegramUser.objects.get_or_create(
                phone=telegram_user_data.get('phone'),
                defaults={'chat_id': telegram_user_data.get('chat_id')}
            )
            instance.telegram_user = telegram_user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.language = language
        new_status = validated_data.get('status', instance.status)
        if new_status and new_status != instance.status:
            instance.update_status(new_status)

        instance.save()

        existing_items = {item.product_id: item for item in instance.order_items.all()}
        for item_data in items_data:
            product_id = item_data.pop('product_id')
            if product_id in existing_items:
                item = existing_items.pop(product_id)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            else:
                OrderItem.objects.create(order=instance, product_id=product_id, **item_data)

        for item in existing_items.values():
            item.delete()

        return instance
        
    class Meta:
        model = Order
        fields = '__all__'
