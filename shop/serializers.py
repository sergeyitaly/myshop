from rest_framework import serializers
from .models import Product, Collection, Category, ProductImage, AdditionalField

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)

    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

class CollectionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False, allow_null=True)
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()
    name = serializers.CharField()
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    description_en = serializers.CharField(required=False)
    description_uk = serializers.CharField(required=False)

    # Use a single method for URL fetching
    def get_photo_url(self, obj):
        return obj.photo.url if obj.photo else None

    def get_photo_thumbnail_url(self, obj):
        return obj.photo_thumbnail.url if obj.photo_thumbnail else None
    
    class Meta:
        model = Collection
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'GET':
            representation.pop('created', None)
            representation.pop('updated', None)
        return representation


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
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()
    collection = CollectionSerializer(required=False, allow_null=True)
    category = CategorySerializer(required=False, allow_null=True)
    images = ProductImageSerializer(source='productimage_set', many=True, read_only=True)
    name = serializers.CharField()
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    description_en = serializers.CharField(required=False)
    description_uk = serializers.CharField(required=False)
    color_name = serializers.CharField(required=False)
    color_name_en = serializers.CharField(required=False)
    color_name_uk = serializers.CharField(required=False)
    additional_fields = AdditionalFieldSerializer(source='additionalfield_set',many=True, read_only=True)
    id_name = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)


    # Use a single method for URL fetching
    def get_photo_url(self, obj):
        return obj.photo.url if obj.photo else None

    def get_photo_thumbnail_url(self, obj):
        return obj.photo_thumbnail.url if obj.photo_thumbnail else None

    class Meta:
        model = Product
        fields = '__all__'

class ProductListSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    photo_thumbnail_url = serializers.SerializerMethodField()
    collection = CollectionSerializer(required=False, allow_null=True)
    category = CategorySerializer(required=False, allow_null=True)
    images = ProductImageSerializer(source='productimage_set', many=True, read_only=True)
    name = serializers.CharField()
    name_en = serializers.CharField(required=False)
    name_uk = serializers.CharField(required=False)
    id_name = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    def get_photo_url(self, obj):
        return obj.photo.url if obj.photo else None

    def get_photo_thumbnail_url(self, obj):
        return obj.photo_thumbnail.url if obj.photo_thumbnail else None

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'GET':
            # Remove fields not needed for the list view
            fields_to_remove = [
                'description', 'description_en', 'description_uk', 'additional_fields',
                'stock', 'slug', 'color_value', 'color_name', 'color_name_en', 
                'color_name_uk', 'brandimage', 'images', 'created', 'updated'
            ]
            for field in fields_to_remove:
                representation.pop(field, None)
        return representation

