from rest_framework import serializers
from .models import Order, OrderItem

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

    class Meta:
        model = Order
        fields = [
            'id', 'name', 'surname', 'phone', 'email', 'address', 'receiver', 'receiver_comments', 
            'submitted_at', 'parent_order', 'present', 'order_items'
        ]

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
