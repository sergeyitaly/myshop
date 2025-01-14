from celery import shared_task
from shop.models import Product
import logging

logger = logging.getLogger(__name__)

@shared_task
def increase_stock_for_unavailable_products():
    updated_count = Product.objects.filter(available=False).update(stock=10, available=True)
    if updated_count > 0:
        logger.info(f"Updated stock for {updated_count} unavailable products.")
    else:
        logger.warning("No unavailable products found to update.")
    return updated_count  # Return the count for further processing or reporting
