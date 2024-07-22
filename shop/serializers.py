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
    photo_thumbnail_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    def get_photo_thumbnail_url(self, obj):
        if obj.photo_thumbnail:
            return obj.photo_thumbnail.url
        return None

    class Meta:
        model = Collection
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    images_thumbnail_url = serializers.SerializerMethodField()

    def get_images_thumbnail_url(self, obj):
        if obj.images_thumbnail:
            return obj.images_thumbnail.url
        return None

    class Meta:
        model = ProductImage
        fields = ['id', 'images', 'images_thumbnail_url']

class AdditionalFieldSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    value = serializers.CharField() 

    class Meta:
        model = AdditionalField
        fields = ['name', 'value']

class ProductSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()
    collection = serializers.ReadOnlyField(source='collection.name')
    images = ProductImageSerializer(source='productimage_set', many=True, read_only=True)
    additional_fields = AdditionalFieldSerializer(many=True, read_only=True)

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    def get_photo_thumbnail_url(self, obj):
        if obj.photo_thumbnail:
            return obj.photo_thumbnail.url
        return None

    class Meta:
        model = Product
        fields = '__all__'

class CreateCollectionSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    def get_photo_thumbnail_url(self, obj):
        if obj.photo_thumbnail:
            return obj.photo_thumbnail.url
        return None

    class Meta:
        model = Collection
        fields = '__all__'
