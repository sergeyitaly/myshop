from celery import shared_task
from shop.models import Product

@shared_task
def increase_stock_for_unavailable_products():
    products = Product.objects.filter(available=False)
    for product in products:
        product.stock = 10
        product.save()
    return f"Updated stock for {products.count()} unavailable products."
