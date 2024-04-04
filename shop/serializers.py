from ast import Delete
from rest_framework import serializers
from .models import Product, Collection



class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('name', 'slug','photo')
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

class ProductSerializer(serializers.ModelSerializer):
    collection = serializers.ReadOnlyField(source='collection.name')
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'collection', 'photo', 'price', 'stock', 'available')

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','collection', 'photo', 'price', 'stock')