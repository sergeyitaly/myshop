# admin.py
from django.contrib import admin
from .models import Collection, Product, Order

admin.site.register(Collection)
admin.site.register(Product)
admin.site.register(Order)
