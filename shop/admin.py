# admin.py
from django.contrib import admin
from .models import Category, Product, Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
