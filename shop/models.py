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
from django.utils.translation import gettext_lazy as _


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
    name = models.CharField(max_length=255, verbose_name=_('Category'), db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Collection(models.Model):
    if USE_S3:
        photo = models.ImageField(upload_to="photos/collection", storage=MediaStorage(), null=True, blank=True, validators=[validate_file_extension], verbose_name = _('photo'))
    else:
        photo = models.ImageField(upload_to="photos/collection", null=True, blank=True, validators=[validate_file_extension], verbose_name = _('photo'))

    photo_thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(50, 50)],
        format='JPEG',
        options={'quality': 60}
    )

    name = models.CharField(max_length=255, verbose_name=_('Collection'), db_index=True)
    category = models.ForeignKey(Category,null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Category'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))
    sales_count = models.PositiveIntegerField(default=0, verbose_name=_('Sales count'))
    products = models.ManyToManyField('Product', related_name='collections', blank=True)

    def image_tag(self):
        if self.photo:
            url = self.photo_thumbnail.url
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(url))
        else:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format('collection.jpg'))

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.photo:
            self.photo.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Collection')
        verbose_name_plural = _('Collections')

    image_tag.short_description =_("Image")
    image_tag.allow_tags = True


class Product(models.Model):
    if USE_S3:
        photo = models.ImageField(upload_to="photos/product", storage=MediaStorage(), null=True, blank=True, validators=[validate_file_extension],  verbose_name=_('photo'))
        brandimage = models.ImageField(upload_to="photos/svg", storage=MediaStorage(), null=True, blank=True, validators=[validate_file_extension],  verbose_name=_('photo'))
    else:
        photo = models.ImageField(upload_to="photos/product", null=True, blank=True, validators=[validate_file_extension],  verbose_name=_('photo'))
        brandimage = models.ImageField(upload_to="photos/svg", null=True, blank=True, validators=[validate_file_extension],  verbose_name=_('photo'))

    photo_thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(50, 50)],
        format='JPEG',
        options={'quality': 60}
    )

    brandimage_thumbnail = ImageSpecField(
        source='brandimage',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60}
    )
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True, db_index=True, verbose_name=_('Collection'))
    name = models.CharField(max_length=255, verbose_name=_('Name'), db_index=True)
    id_name = models.CharField(max_length=255, verbose_name=_('ID Name'), db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    price = models.DecimalField(max_digits=10, decimal_places=1, verbose_name=_('Price'), default=0.0, db_index=True)
    stock = models.PositiveIntegerField(default=0, verbose_name=_('Stock'))
    available = models.BooleanField(default=True, verbose_name=_('Available'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))
    sales_count = models.PositiveIntegerField(default=0, verbose_name=_('Sales Count'), db_index=True)
    popularity = models.PositiveIntegerField(default=0, verbose_name=_('Popularity'), db_index=True)
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    color_name = models.CharField(max_length=50, null=True, blank=True, help_text=_("Enter the color name, e.g., magenta or purple"), verbose_name=_('Color Name'))
    color_value = ColorField(default='#RRGGBB', null=True, blank=True, help_text=_("Enter the color value in the format #RRGGBB"), verbose_name=_('Color Value'))
    size = models.CharField(max_length=50, null=True, blank=True, help_text=_("Format: LxHxD (in mm or specify cm)"), verbose_name=_('Size'))
    discount = models.DecimalField(max_digits=5, decimal_places=2, db_index=True, default=0.00, null=True, blank=True, help_text=_("Discount percentage (e.g., 10.00 for 10%)"), verbose_name=_('Discount'))

    CURRENCY_CHOICES = (
        ('UAH', 'UAH (грн)'),
        ('USD', 'USD ($)'),
        ('EUR', 'EUR (€)'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='UAH', verbose_name=_('Currency'))

    def image_tag(self):
        if self.photo:
            url = self.photo_thumbnail.url
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(url))
        else:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format('product.png'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()

        if not self.id_name:
            name_with_underscores = self.name.replace(' ', '_')
            self.id_name = f"{self.id}_{name_with_underscores}"
        
        super().save(*args, **kwargs)
        if not self.id_name:
            self.id_name = f"{self.id}_{name_with_underscores}"
            self.save(update_fields=['id_name'])

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
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    image_tag.short_description = _("Image")
    image_tag.allow_tags = True

class ProductImage(models.Model):
    if USE_S3:
        images = models.FileField(upload_to='photos/product', storage=MediaStorage(), validators=[validate_file_extension], verbose_name=_('images'))
    else:
        images = models.FileField(upload_to='photos/product', validators=[validate_file_extension], verbose_name=_('images'))

    images_thumbnail = ImageSpecField(
        source='images',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60}
    )

    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
#    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='product_images')

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

class AdditionalField(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'), null=True, blank=True,db_index=True)
    value = models.TextField(verbose_name=_('value'),null=True, blank=True)
 #   product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Product'))
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, verbose_name=_('Product'))


    def __str__(self):
        return self.name
    
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
