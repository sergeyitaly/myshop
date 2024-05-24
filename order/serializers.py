from rest_framework import serializers
from .models import Order, OrderItem
from shop.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'collection']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source='product', 
        queryset=Product.objects.all(), 
        write_only=True
    )  # Reference product by ID for creation

    class Meta:
        model = OrderItem
        fields = ['product', 'product_id', 'quantity', 'price']

    def create(self, validated_data):
        product = validated_data.pop('product')
        price = product.price
        return OrderItem.objects.create(product=product, price=price, **validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'items', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
