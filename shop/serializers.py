from ast import Delete
from rest_framework import serializers
from .models import Product, Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug','photo')
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'photo', 'color', 'price', 'stock', 'available')

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','category', 'photo', 'color','price', 'stock')