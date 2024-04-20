from ast import Delete
from rest_framework import serializers
from .models import Product, Collection, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

class CollectionSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    photo_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None
    class Meta:
        model = Collection
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None
    class Meta:
        model = Product
        fields = '__all__'

class CreateCollectiontSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None
    class Meta:
        model = Product
        fields = '__all__'