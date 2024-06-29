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
        fields = ['name','surname', 'email', 'address', 'order_items']

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product_id = item_data.pop('product_id')
            OrderItem.objects.create(order=order, product_id=product_id, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_items')
        instance.name = validated_data.get('name', instance.name)
        instance.name = validated_data.get('name', instance.name)

        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        # Delete existing order items
        instance.order_items.all().delete()

        # Create new order items
        for item_data in items_data:
            product_id = item_data.pop('product_id')
            OrderItem.objects.create(order=instance, product_id=product_id, **item_data)

        return instance
