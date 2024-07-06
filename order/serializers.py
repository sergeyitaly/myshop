# shop/serializers.py

from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        order_item = OrderItem.objects.create(product_id=product_id, **validated_data)
        return order_item


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments', 'submitted_at', 'parent_order', 'present', 'order_items']

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product_id = item_data.pop('product_id')
            OrderItem.objects.create(order=order, product_id=product_id, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items', [])
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.receiver = validated_data.get('receiver', instance.receiver)
        instance.receiver_comments = validated_data.get('receiver_comments', instance.receiver_comments)
        instance.parent_order = validated_data.get('parent_order', instance.parent_order)
        instance.present = validated_data.get('present', instance.present)
        instance.save()

        # Delete existing order items
        instance.order_items.all().delete()

        # Create new order items
        for item_data in items_data:
            product_id = item_data.pop('product_id')
            OrderItem.objects.create(order=instance, product_id=product_id, **item_data)

        return instance
