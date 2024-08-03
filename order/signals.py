from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import is_aware, make_naive
from .models import Order, OrderSummary, OrderItem

def datetime_to_str(dt):
    if dt:
        if is_aware(dt):
            dt = make_naive(dt)
        return dt.strftime('%Y-%m-%d %H:%M')
    return None

def safe_make_naive(dt):
    if dt is None:
        return None
    return make_naive(dt) if is_aware(dt) else dt

def get_order_summary(order):
    submitted_at = safe_make_naive(order.submitted_at)
    processed_at = safe_make_naive(order.processed_at)
    completed_at = safe_make_naive(order.completed_at)
    canceled_at = safe_make_naive(order.canceled_at)

    # Convert datetime fields to formatted string
    summary = {
        'order_id': order.id,
        'submitted_at': datetime_to_str(submitted_at),
        'processed_at': datetime_to_str(processed_at),
        'completed_at': datetime_to_str(completed_at),
        'canceled_at': datetime_to_str(canceled_at),
        'order_items': [
            {
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': item.price
            }
            for item in order.order_items.all()
        ]
    }
    return summary

def update_order_summary_for_chat_id(chat_id):
    if chat_id:
        order_summary, created = OrderSummary.objects.get_or_create(chat_id=chat_id)
        orders = [get_order_summary(order) for order in Order.objects.filter(telegram_user__chat_id=chat_id)]
        order_summary.orders = orders
        order_summary.save()

@receiver(post_save, sender=Order)
def update_order_summary(sender, instance, **kwargs):
    chat_id = instance.telegram_user.chat_id if instance.telegram_user else None
    update_order_summary_for_chat_id(chat_id)

@receiver(post_save, sender=OrderItem)
def update_order_summary_on_order_item_change(sender, instance, **kwargs):
    order = instance.order
    chat_id = order.telegram_user.chat_id if order.telegram_user else None
    update_order_summary_for_chat_id(chat_id)

@receiver(post_delete, sender=Order)
def remove_order_from_summary(sender, instance, **kwargs):
    chat_id = instance.telegram_user.chat_id if instance.telegram_user else None
    if chat_id:
        try:
            order_summary = OrderSummary.objects.get(chat_id=chat_id)
            order_summary.orders = [order for order in order_summary.orders if order['order_id'] != instance.id]
            order_summary.save()
        except OrderSummary.DoesNotExist:
            pass

@receiver(post_delete, sender=OrderItem)
def update_order_summary_on_order_item_delete(sender, instance, **kwargs):
    order = instance.order
    chat_id = order.telegram_user.chat_id if order.telegram_user else None
    update_order_summary_for_chat_id(chat_id)
