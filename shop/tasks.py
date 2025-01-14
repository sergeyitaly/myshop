from celery import shared_task
from shop.models import Product

@shared_task
def increase_stock_for_unavailable_products():
    # Perform a bulk update for all unavailable products
    updated_count = Product.objects.filter(available=False).update(stock=10, available=True)
        # Log the number of updated products
    return f"Updated stock for {updated_count} unavailable products."
