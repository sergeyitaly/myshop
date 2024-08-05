from rest_framework import serializers
from .models import *

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
        # Ensure Decimal values are serialized properly if necessary
        representation['orders'] = self._convert_decimals(representation['orders'])
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
    product_id = serializers.IntegerField(write_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    collection_name = serializers.CharField(source='product.collection.name', read_only=True)
    size = serializers.CharField(source='product.size', read_only=True)
    color_name = serializers.CharField(source='product.color_name', read_only=True)
    color_value = serializers.CharField(source='product.color_value', read_only=True)
    item_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_sum = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity', 'product_name', 'collection_name', 'size', 'color_name', 'color_value', 'item_price', 'total_sum']

    def get_total_sum(self, obj):
        return obj.quantity * obj.product.price

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        order_item = OrderItem.objects.create(product_id=product_id, **validated_data)
        return order_item

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    chat_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Order
        fields = [
            'id', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments',
            'submitted_at', 'created_at', 'processed_at', 'complete_at', 'canceled_at', 'parent_order',
            'present', 'status', 'order_items', 'chat_id'
        ]



def create(self, validated_data):
    items_data = validated_data.pop('order_items')
    telegram_user_data = validated_data.pop('telegram_user', None)
    
    if telegram_user_data:
        telegram_user, created = TelegramUser.objects.get_or_create(
            phone=telegram_user_data['phone'],
            defaults={'chat_id': telegram_user_data['chat_id']}
        )
    else:
        telegram_user = None

    # Create the Order instance
    order = Order.objects.create(telegram_user=telegram_user, **validated_data)

    # Now that the Order instance is saved and has an ID, create related OrderItems
    for item_data in items_data:
        product_id = item_data.pop('product_id')
        OrderItem.objects.create(order=order, product_id=product_id, **item_data)

    return order
def update(self, instance, validated_data):
    items_data = validated_data.pop('order_items', [])
    telegram_user_data = validated_data.pop('telegram_user', None)

    if telegram_user_data:
        telegram_user, created = TelegramUser.objects.get_or_create(
            phone=telegram_user_data['phone'],
            defaults={'chat_id': telegram_user_data['chat_id']}
        )
        instance.telegram_user = telegram_user

    # Update the Order instance
    for attr, value in validated_data.items():
        setattr(instance, attr, value)

    new_status = validated_data.get('status', instance.status)
    if new_status and new_status != instance.status:
        instance.update_status(new_status)

    instance.save()

    # Delete existing OrderItems and add updated ones
    instance.order_items.all().delete()
    for item_data in items_data:
        product_id = item_data.pop('product_id')
        OrderItem.objects.create(order=instance, product_id=product_id, **item_data)

    return instance
