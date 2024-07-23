import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.utils.text import slugify
from storages.backends.s3boto3 import S3Boto3Storage
from dotenv import load_dotenv
from distutils.util import strtobool
from django.core.files.images import get_image_dimensions
from colorfield.fields import ColorField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import post_save
from django.dispatch import receiver


load_dotenv()
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_MEDIA_LOCATION = os.getenv('AWS_MEDIA', 'media')
USE_S3 = bool(strtobool(os.getenv('USE_S3', 'True')))
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{AWS_MEDIA_LOCATION}/'

class MediaStorage(S3Boto3Storage):
    location = AWS_MEDIA_LOCATION
    file_overwrite = True

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.svg']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def validate_image(value):
    try:
        width, height = get_image_dimensions(value)
    except AttributeError:
        raise ValidationError("The file is not an image.")

def validate_svg(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.svg':
        raise ValidationError('Unsupported file extension.')

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Collection(models.Model):
    if USE_S3:
        photo = models.ImageField(upload_to="photos/collection", storage=MediaStorage(), null=True, blank=True, validators=[validate_file_extension])
    else:
        photo = models.ImageField(upload_to="photos/collection", null=True, blank=True, validators=[validate_file_extension])

    photo_thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60}
    )

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sales_count = models.PositiveIntegerField(default=0)

    def image_tag(self):
        if self.photo:
            url = self.photo_thumbnail.url
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(url))
        else:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format('default_collection.jpg'))

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.photo:
            self.photo.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

class AdditionalField(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='additional_fields')

    def __str__(self):
        return f"{self.name} - {self.value}"

class Product(models.Model):
    if USE_S3:
        photo = models.ImageField(upload_to="photos/product", storage=MediaStorage(), null=True, blank=True, validators=[validate_file_extension])
        brandimage = models.ImageField(upload_to="photos/svg", storage=MediaStorage(), null=True, blank=True, validators=[validate_file_extension])
    else:
        photo = models.ImageField(upload_to="photos/product", null=True, blank=True, validators=[validate_file_extension])
        brandimage = models.ImageField(upload_to="photos/svg", null=True, blank=True, validators=[validate_file_extension])

    photo_thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60}
    )

    brandimage_thumbnail = ImageSpecField(
        source='brandimage',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60}
    )

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sales_count = models.PositiveIntegerField(default=0)
    popularity = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)
    color_name = models.CharField(max_length=50, null=True, blank=True, help_text="Enter the color name, e.g., magenta or purple")
    color_value = ColorField(default='#RRGGBB', null=True, blank=True, help_text="Enter the color value in the format #RRGGBB")
    size = models.CharField(max_length=50, null=True, blank=True, help_text="Format: LxHxD (in mm or specify cm)")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, null=True, blank=True, help_text="Discount percentage (e.g., 10.00 for 10%)")

    CURRENCY_CHOICES = (
        ('UAH', 'UAH (грн)'),
        ('USD', 'USD ($)'),
        ('EUR', 'EUR (€)'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UAH')

    def image_tag(self):
        if self.photo:
            url = self.photo_thumbnail.url
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(url))
        else:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format('default_product.png'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        if not base_slug:
            base_slug = f'product-{self.pk}'
        slug = base_slug
        num = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{num}'
            num += 1
        return slug

    def delete(self, *args, **kwargs):
        if self.photo:
            self.photo.delete(save=False)
        if self.brandimage:
            self.brandimage.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

class ProductImage(models.Model):
    if USE_S3:
        images = models.FileField(upload_to='photos/product', storage=MediaStorage(), validators=[validate_file_extension])
    else:
        images = models.FileField(upload_to='photos/product', validators=[validate_file_extension])

    images_thumbnail = ImageSpecField(
        source='images',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60}
    )

    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if self.images:
            filename = os.path.basename(self.images.name)
            self.images.name = filename  # Save the filename exactly as it is
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.images:
            self.images.delete(save=False)
        super().delete(*args, **kwargs)


from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Collection)
def generate_collection_thumbnails(sender, instance, **kwargs):
    if instance.photo:
        instance.photo_thumbnail.generate()

@receiver(post_save, sender=Product)
def generate_product_thumbnails(sender, instance, **kwargs):
    if instance.photo:
        instance.photo_thumbnail.generate()
    if instance.brandimage:
        instance.brandimage_thumbnail.generate()

@receiver(post_save, sender=ProductImage)
def generate_product_image_thumbnails(sender, instance, **kwargs):
    if instance.images:
        instance.images_thumbnail.generate()
