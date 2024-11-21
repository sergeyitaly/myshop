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
#    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False, write_only=True)

    total_sum = serializers.SerializerMethodField()

    # Other fields related to the product
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=1, read_only=True)
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
            'product_id', 'quantity', 'price', 'color_value', 'size', 'total_sum',
            'name_en', 'color_name_en', 'collection_name_en', 'name_uk', 'color_name_uk', 'collection_name_uk'
        ]

    def get_total_sum(self, obj):
        return obj.total_sum  # Return total_sum directly
        
    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        return OrderItem.objects.create(product_id=product_id, **validated_data)
    


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)
    telegram_user = serializers.PrimaryKeyRelatedField(queryset=TelegramUser.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            # Remove unnecessary read-only fields for POST requests
            self.fields.pop('order_items_en', None)
            self.fields.pop('order_items_uk', None)


    def create(self, validated_data):
        # Print the validated data to ensure it's correct
        print("Start creating order with validated_data:", validated_data)
        
        # Extract and print order items
        items_data = validated_data.pop('order_items', [])
        print("Extracted items_data:", items_data)

        # Extract and print telegram user data
        telegram_user_data = validated_data.pop('telegram_user', None)
        print("Extracted telegram_user_data:", telegram_user_data)

        telegram_user = None
        if telegram_user_data:
            print(f"Attempting to fetch or create TelegramUser with phone: {telegram_user_data.get('phone')}")
            
            # Fetch or create the TelegramUser and print the result
            telegram_user, created = TelegramUser.objects.get_or_create(
                phone=telegram_user_data.get('phone'),
                defaults={'chat_id': telegram_user_data.get('chat_id')}
            )
            print(f"Fetched/created telegram_user: {telegram_user} (created: {created})")
        
        # Create the order and print the result
        print(f"Creating Order with telegram_user: {telegram_user}")
        order = Order.objects.create(telegram_user=telegram_user, **validated_data)
        print(f"Created order: {order}")

        # Process each item and print each step
        for item_data in items_data:
            print(f"Processing item_data: {item_data}")
            
            product_id = item_data.pop('product_id', None)
            if not product_id:
                print(f"Error: Missing product_id in item_data: {item_data}")
                raise ValidationError("product_id is required for order items.")

            try:
                # Ensure the product exists
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                print(f"Error: Product with id {product_id} not found.")
                raise ValidationError(f"Product with id {product_id} does not exist.")

            # Create the order item and print the result
            order_item = OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'])
            print(f"Created OrderItem with product_id: {product_id}, OrderItem: {order_item}")

        return order


    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items', [])
        telegram_user_data = validated_data.pop('telegram_user', None)

        if telegram_user_data:
            telegram_user, created = TelegramUser.objects.get_or_create(
                phone=telegram_user_data.get('phone'),
                defaults={'chat_id': telegram_user_data.get('chat_id')}
            )
            instance.telegram_user = telegram_user

        # Update the Order instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        new_status = validated_data.get('status', instance.status)
        if new_status and new_status != instance.status:
            instance.update_status(new_status)

        instance.save()

        # Update OrderItems
        existing_items = {item.product_id: item for item in instance.order_items.all()}
        for item_data in items_data:
            product_id = item_data.pop('product_id')
            if product_id in existing_items:
                # Update existing item
                item = existing_items.pop(product_id)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            else:
                # Create new item
                OrderItem.objects.create(order=instance, product_id=product_id, **item_data)

        # Delete any items not in the updated list
        for item in existing_items.values():
            item.delete()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        order_items_en, order_items_uk = self._get_order_items(instance)
        representation['order_items_en'] = order_items_en
        representation['order_items_uk'] = order_items_uk
        return representation

    def _get_order_items(self, obj):
        items_en = []
        items_uk = []
        for item in obj.order_items.all():
            product = item.product

            # Default values
            default_name = _("No Name")
            default_color = _("No Color")
            default_collection = _("No Collection")

            item_data_en = {
                'size': product.size,
                'quantity': item.quantity,
                'price': float(product.price),
                'color_value': product.color_value,
                'name': product.name_en or default_name,
                'color_name': product.color_name_en or default_color,
                'collection_name': (product.collection.name_en if product.collection else None) or default_collection,
                'total_sum': str(item.total_sum),
            }

            item_data_uk = {
                'size': product.size,
                'quantity': item.quantity,
                'price': float(product.price),
                'color_value': product.color_value,
                'name': product.name_uk or default_name,
                'color_name': product.color_name_uk or default_color,
                'collection_name': (product.collection.name_uk if product.collection else None) or default_collection,
                'total_sum': str(item.total_sum),
            }

            items_en.append(item_data_en)
            items_uk.append(item_data_uk)

        return items_en, items_uk

    class Meta:
        model = Order
        fields = '__all__'
