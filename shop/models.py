# models.py

import os
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import truncatechars 
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify # new


class Collection(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    photo = models.ImageField(upload_to="photos/banner", null=True, blank=True)

    @property
    def short_description(self):
        return truncatechars(self.description, 20)    
    
    def image_tag(self):
        if self.photo:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.photo.url))
        else:
            return '(No image)'   
    image_tag.short_description = "Image"
    image_tag.allow_tags = True
    
    def __str__(self):
        return self.name    

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Product(models.Model):

    category = models.ForeignKey(Collection, on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=300, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
   
    photo = models.ImageField(upload_to="photos", null=True, blank=True)
    brandimage = models.FileField(upload_to="photos/svg", null=True, blank=True)
   
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    @property
    def short_description(self):
        return truncatechars(self.description, 20)    
    
    def image_tag(self):
        if self.photo:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.photo.url))
        else:
            return '(No image)'    
    
    image_tag.short_description = "Image"
    image_tag.allow_tags = True

class Order(models.Model):
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add more fields as needed
