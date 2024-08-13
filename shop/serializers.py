from rest_framework import serializers
from .models import Product, Collection, Category, ProductImage, AdditionalField

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'name_en', 'name_uk']
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

class CollectionSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()
    name = serializers.CharField()
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    description_en = serializers.CharField(required=False)
    description_uk = serializers.CharField(required=False)

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo:
            photo_url = request.build_absolute_uri(obj.photo.url)
            print(f"Generated photo URL: {photo_url}")
            return photo_url
        return request.build_absolute_uri('photos/collection/default_collection.jpg')

    def get_photo_thumbnail_url(self, obj):
        if obj.photo_thumbnail:
            photo_thumbnail_url = obj.photo_thumbnail.url
            print(f"Generated thumbnail URL: {photo_thumbnail_url}")
            return photo_thumbnail_url
        return None
    
    class Meta:
        model = Collection
        fields = [
            'id', 'name', 'name_en', 'name_uk', 'description', 'description_en', 'description_uk',
            'photo_url', 'photo_thumbnail_url', 'category'
        ]

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
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)
    value = serializers.CharField()
    value_en = serializers.CharField(required=False)
    value_uk = serializers.CharField(required=False)

    class Meta:
        model = AdditionalField
        fields = ['id', 'name', 'name_en', 'name_uk', 'value', 'value_en', 'value_uk']

class ProductSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()
    collection = serializers.ReadOnlyField(source='collection.name')
    images = ProductImageSerializer(source='productimage_set', many=True, read_only=True)
    additional_fields = AdditionalFieldSerializer(many=True, read_only=True)
    name = serializers.CharField()
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    description_en = serializers.CharField(required=False)
    description_uk = serializers.CharField(required=False)
    color_name = serializers.CharField(required=False)
    color_name_en = serializers.CharField(required=False)
    color_name_uk = serializers.CharField(required=False)

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
        fields = [
            'id', 'name', 'name_en', 'name_uk', 'description', 'description_en', 'description_uk',
            'color_name', 'color_name_en', 'color_name_uk', 'photo_url', 'photo_thumbnail_url',
            'collection', 'images', 'additional_fields'
        ]