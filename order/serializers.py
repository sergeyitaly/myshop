from rest_framework import serializers
from .models import *
import decimal

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
    color_value = serializers.CharField(source='product.color.value', read_only=True)

    # Assuming the 'color' is a related model (e.g., ForeignKey or OneToOne field)
    color_name = serializers.CharField(source='product.color.name', read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    collection_name = serializers.CharField(source='product.collection.name', read_only=True)

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
        fields = ['product_id', 'product', 'quantity', 'total_sum', 'price', 'color_value',
                  'name','color_name', 'collection_name'
                  ]


class OrderSerializer(serializers.ModelSerializer):
    order_items_uk = OrderItemSerializer(many=True, required=False)
    order_items_en = OrderItemSerializer(many=True, required=False)
    telegram_user = TelegramUserSerializer(required=False, allow_null=True)

    class Meta:
        model = Order
        fields = [
            'id', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments',
            'congrats', 'submitted_at', 'created_at', 'processed_at', 'complete_at', 'canceled_at',
            'parent_order', 'present', 'status', 'order_items_uk', 'order_items_en', 'telegram_user'
        ]

    def create(self, validated_data):
        # Separate the order_items by language
        order_items_uk_data = validated_data.pop('order_items_uk', [])
        order_items_en_data = validated_data.pop('order_items_en', [])
        telegram_user_data = validated_data.pop('telegram_user', None)
        
        # Handle telegram_user creation if provided
        telegram_user = None
        if telegram_user_data:
            telegram_user, created = TelegramUser.objects.get_or_create(
                phone=telegram_user_data['phone'],
                defaults={'chat_id': telegram_user_data['chat_id']}
            )

        # Create the Order instance
        order = Order.objects.create(telegram_user=telegram_user, **validated_data)

        # Create related OrderItems for 'uk'
        for item_data in order_items_uk_data:
            product_id = item_data.pop('product_id')
            OrderItem.objects.create(order=order, product_id=product_id, **item_data)

        # Create related OrderItems for 'en'
        for item_data in order_items_en_data:
            product_id = item_data.pop('product_id')
            OrderItem.objects.create(order=order, product_id=product_id, **item_data)

        return order

    def update(self, instance, validated_data):
        # Update all standard fields on the Order instance
        for attr, value in validated_data.items():
            if attr != 'order_items':  # Skip `order_items` for now
                setattr(instance, attr, value)

        # Save updated instance fields before handling related data
        instance.save()

        # Handle `order_items` dynamically, regardless of language
        if 'order_items' in validated_data:
            updated_items_data = validated_data.pop('order_items')
            
            # Create a map of existing items by product_id for efficient updating
            existing_items = {item.product_id: item for item in instance.order_items.all()}
            
            # Process updated items
            for item_data in updated_items_data:
                product_id = item_data.pop('product_id')
                
                if product_id in existing_items:
                    # Update existing item
                    existing_item = existing_items.pop(product_id)
                    for key, value in item_data.items():
                        setattr(existing_item, key, value)
                    existing_item.save()
                else:
                    # Create new item if it doesn't exist
                    OrderItem.objects.create(order=instance, product_id=product_id, **item_data)

            # Delete any items that were not in the updated data
            for remaining_item in existing_items.values():
                remaining_item.delete()

        return instance
