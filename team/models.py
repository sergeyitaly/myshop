from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os
from dotenv import load_dotenv
from distutils.util import strtobool
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.html import format_html
from django.db.models.signals import post_save
from django.dispatch import receiver

# Load environment variables
load_dotenv()

# AWS and Media Settings
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_MEDIA_LOCATION = os.getenv('AWS_MEDIA_LOCATION', 'media')
USE_S3 = bool(strtobool(os.getenv('USE_S3', 'True')))
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{AWS_MEDIA_LOCATION}/' if USE_S3 else '/media/'

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

class TeamMember(models.Model):
    name = models.CharField(max_length=100,  verbose_name=_('Name'))
    surname = models.CharField(max_length=100, verbose_name=_('Surname'))
    mobile = models.CharField(max_length=15, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    
    if USE_S3:
        photo = models.ImageField(upload_to="photos/team", storage=MediaStorage(), null=True, blank=True, validators=[validate_file_extension], verbose_name=_('photo'))
    else:
        photo = models.ImageField(upload_to="photos/team", null=True, blank=True, validators=[validate_file_extension], verbose_name=_('photo'))

    photo_thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(50, 50)],
        format='JPEG',
        options={'quality': 60}
    )

    def image_tag(self):
        if self.photo and hasattr(self.photo, 'url'):
            try:
                url = self.photo_thumbnail.url
                return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format(url))
            except Exception:
                return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format('default_photo.jpg'))
        else:
            return format_html('<img src="{}" style="max-height: 150px; max-width: 150px;" />'.format('default_photo.jpg'))

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo:
            self.photo.delete(save=False)
        super().delete(*args, **kwargs)

# Move the signal outside the class to avoid the NameError
@receiver(post_save, sender=TeamMember)
def generate_teammember_thumbnails(sender, instance, **kwargs):
    if instance.photo:
        instance.photo_thumbnail.generate()

class Meta:
    ordering = ('name',)
    verbose_name = _('TeamMember')
    verbose_name_plural = _('TeamMembers')
