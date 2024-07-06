from rest_framework import serializers
from .models import Product, Collection, Category, ProductImage, AdditionalField

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

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'images']

class AdditionalFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalField
        fields = ['name', 'value']

class ProductSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    collection = serializers.ReadOnlyField(source='collection.name')
    images = ProductImageSerializer(source='productimage_set', many=True, read_only=True)
    additional_fields = AdditionalFieldSerializer(many=True, read_only=True)

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    class Meta:
        model = Product
        fields = '__all__'

class CreateCollectionSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    class Meta:
        model = Collection
        fields = '__all__'
