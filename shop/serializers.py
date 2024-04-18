from ast import Delete
from rest_framework import serializers
from .models import Product, Collection, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

class CollectionSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Collection
        fields = ('id','name', 'category','slug','photo')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'slug', 'photo', 'price', 'stock', 'available')

class CreateCollectiontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'category', 'photo', 'price', 'stock')