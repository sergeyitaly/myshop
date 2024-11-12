from rest_framework import serializers
from .models import *
import decimal

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['id', 'phone', 'chat_id']

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
    total_sum = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

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

        # Add the product to the validated data
        data['product'] = product
        return data

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product', 'quantity', 'total_sum']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=True)
    telegram_user = TelegramUserSerializer(required=False, allow_null=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, attrs):
        if not attrs.get('order_items'):
            raise serializers.ValidationError("Order must contain at least one item with a valid product.")
        
        # Validate chat_id if telegram_user is provided
        telegram_user_data = attrs.get('telegram_user')
        if telegram_user_data and not telegram_user_data.get('chat_id'):
            raise serializers.ValidationError({"telegram_user": "chat_id is required for the TelegramUser."})
        
        return attrs
    
    def create(self, validated_data):
        items_data = validated_data.pop('order_items', [])
        telegram_user_data = validated_data.pop('telegram_user', None)

        # Create the order instance
        order = Order.objects.create(**validated_data)

        # Create order items
        for item_data in items_data:
            # Extract product_id from item_data, ensure it's used for product lookup
            product_id = item_data.pop('product_id', None)
            if not product_id:
                raise serializers.ValidationError("Product ID must be provided.")

            # Ensure 'product' is not in item_data before creating the OrderItem
            item_data.pop('product', None)

            try:
                # Get the product instance
                product_instance = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")

            # Calculate the total sum for the item
            item_data['total_sum'] = product_instance.price * item_data.get('quantity', 1)

            # Create OrderItem and associate the product explicitly
            OrderItem.objects.create(order=order, product=product_instance, **item_data)

        # Handle telegram_user if provided
        if telegram_user_data:
            # Get or create the TelegramUser instance
            telegram_user, created = TelegramUser.objects.get_or_create(
                phone=telegram_user_data['phone'],
                defaults={'chat_id': telegram_user_data.get('chat_id')}  # Make sure to pass chat_id in defaults
            )

            # If the user already exists, update chat_id if it is provided
            if not created and telegram_user_data.get('chat_id'):
                telegram_user.chat_id = telegram_user_data['chat_id']
                telegram_user.save()

            # Link the TelegramUser to the order
            order.telegram_user = telegram_user
            order.save()  # Save the order after linking the telegram_user

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items', [])
        telegram_user_data = validated_data.pop('telegram_user', None)

        # Update telegram_user if provided
        if telegram_user_data:
            telegram_user, created = TelegramUser.objects.get_or_create(
                phone=telegram_user_data['phone'],
                defaults={'chat_id': telegram_user_data.get('chat_id')}
            )

            if not created and telegram_user_data.get('chat_id'):
                telegram_user.chat_id = telegram_user_data['chat_id']
                telegram_user.save()

            instance.telegram_user = telegram_user

        # Update other fields on the order
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Handle order items update
        existing_items = {item.product.id: item for item in instance.order_items.all()}
        for item_data in items_data:
            product = item_data.pop('product')
            if not Product.objects.filter(id=product.id).exists():
                raise serializers.ValidationError(f"Product with ID {product.id} does not exist.")

            if product.id in existing_items:
                item = existing_items.pop(product.id)
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            else:
                item_data['total_sum'] = product.price * item_data['quantity']
                OrderItem.objects.create(order=instance, product=product, **item_data)

        # Delete removed order items
        for item in existing_items.values():
            item.delete()

        return instance
