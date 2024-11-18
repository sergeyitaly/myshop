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
            product_id = item_data.pop('product_id', None)
            if not product_id:
                raise serializers.ValidationError("Product ID must be provided.")
            item_data.pop('product', None)

            try:
                product_instance = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with ID {product_id} does not exist.")

            item_data['total_sum'] = product_instance.price * item_data.get('quantity', 1)
            OrderItem.objects.create(order=order, product=product_instance, **item_data)

        # Handle telegram_user based on phone number if provided
        phone = validated_data.get('phone')
        if phone:
            try:
                telegram_user = TelegramUser.objects.get(phone=phone)
            except TelegramUser.DoesNotExist:
                telegram_user = None  # Optionally handle creation or other behavior if user not found

            if telegram_user:
                order.telegram_user = telegram_user  # Link TelegramUser to the order
                order.save()

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items', [])
        telegram_user_data = validated_data.pop('telegram_user', None)

        # Update other fields on the order
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle telegram_user based on phone number if provided
        phone = validated_data.get('phone')
        if phone:
            try:
                telegram_user = TelegramUser.objects.get(phone=phone)
            except TelegramUser.DoesNotExist:
                telegram_user = None  # Optionally handle creation or other behavior if user not found

            if telegram_user:
                instance.telegram_user = telegram_user  # Link TelegramUser to the order
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
